use serde::{Deserialize, Serialize};
use std::process::Stdio;
use std::sync::Arc;
use tauri::{AppHandle, Emitter, Manager, State};
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;
use tokio::sync::Mutex;
use tokio::time::{timeout, Duration};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ChatMessage {
    pub role: String,
    pub content: String,
    pub timestamp: Option<String>,
}

pub struct AppState {
    pub mimo_process: Arc<Mutex<Option<tokio::process::Child>>>,
    pub mimo_stdin: Arc<Mutex<Option<tokio::process::ChildStdin>>>,
    pub request_id: Arc<Mutex<u64>>,
    pub is_connected: Arc<Mutex<bool>>,
    pub conversation_id: Arc<Mutex<Option<String>>>,
}

impl AppState {
    pub fn new() -> Self {
        Self {
            mimo_process: Arc::new(Mutex::new(None)),
            mimo_stdin: Arc::new(Mutex::new(None)),
            request_id: Arc::new(Mutex::new(10)), // Start with a safe ID
            is_connected: Arc::new(Mutex::new(false)),
            conversation_id: Arc::new(Mutex::new(None)),
        }
    }
}

async fn clean_up_arcs(
    mimo_process: Arc<Mutex<Option<tokio::process::Child>>>,
    mimo_stdin: Arc<Mutex<Option<tokio::process::ChildStdin>>>,
    is_connected: Arc<Mutex<bool>>,
    conversation_id: Arc<Mutex<Option<String>>>,
) {
    {
        let mut process_guard = mimo_process.lock().await;
        if let Some(mut child) = process_guard.take() {
            let _ = child.kill().await;
            let _ = child.wait().await;
            println!("mimo acp 자식 프로세스 안전 종료됨");
        }
    }
    
    {
        let mut stdin_guard = mimo_stdin.lock().await;
        *stdin_guard = None;
    }
    
    {
        let mut connected = is_connected.lock().await;
        *connected = false;
    }
    
    {
        let mut conv_id = conversation_id.lock().await;
        *conv_id = None;
    }
}

#[tauri::command]
async fn connect_mimo(state: State<'_, AppState>, app: AppHandle) -> Result<String, String> {
    // Always clean up any existing process/connection to avoid orphaned processes across reloads
    clean_up_arcs(
        state.mimo_process.clone(),
        state.mimo_stdin.clone(),
        state.is_connected.clone(),
        state.conversation_id.clone(),
    ).await;

    let mimo_path = "/Users/tedchanglimchangsik/.mimocode/bin/mimo";
    
    // Inject environment variables directly to avoid GUI startup inheritance issues
    // and bypass shell initialization delays (which caused stdin race conditions).
    let mut child = Command::new(mimo_path)
        .arg("acp")
        .arg("--print-logs")
        .arg("--cwd")
        .arg("/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared")
        .current_dir("/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared")
        .env("MIMO_API_KEY", "sk-sho2gjhe0thboan84dnepjy1lx2ueqpbw8yv6tjsmanna56r")
        .env("MIMO_BASE_URL", "http://127.0.0.1:1984/v1")
        .env("XIAOMI_API_KEY", "sk-sho2gjhe0thboan84dnepjy1lx2ueqpbw8yv6tjsmanna56r")
        .env("XIAOMI_BASE_URL", "http://127.0.0.1:1984/v1")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("mimo acp 프로세스 실행 실패: {}", e))?;

    let mut stdin = child.stdin.take().ok_or("stdin을 열 수 없습니다")?;
    let stdout = child.stdout.take().ok_or("stdout을 열 수 없습니다")?;
    let stderr = child.stderr.take().ok_or("stderr을 열 수 없습니다")?;

    // Send the initialize request immediately to kick off the ACP handshake
    let initialize_req = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": 1
        }
    });
    
    use tokio::io::AsyncWriteExt;
    let req_str = format!("{}\n", serde_json::to_string(&initialize_req).unwrap());
    
    let write_res = timeout(Duration::from_secs(5), async {
        stdin.write_all(req_str.as_bytes()).await?;
        stdin.flush().await?;
        Ok::<(), std::io::Error>(())
    }).await;

    if write_res.is_err() || write_res.unwrap().is_err() {
        let _ = child.kill().await;
        return Err("initialize 송신 실패 (시간 초과 또는 파이프 오류)".to_string());
    }

    // Store stdin and child in AppState
    {
        let mut stdin_lock = state.mimo_stdin.lock().await;
        *stdin_lock = Some(stdin);
    }
    
    {
        let mut process_lock = state.mimo_process.lock().await;
        *process_lock = Some(child);
    }

    // Spawn reader task
    let app_clone = app.clone();
    let is_connected_clone = state.is_connected.clone();
    let conversation_id_clone = state.conversation_id.clone();
    let mimo_stdin_clone = state.mimo_stdin.clone();
    let mimo_process_clone = state.mimo_process.clone();

    let mimo_process_reader = mimo_process_clone.clone();
    let mimo_stdin_reader = mimo_stdin_clone.clone();
    let is_connected_reader = is_connected_clone.clone();
    let conversation_id_reader = conversation_id_clone.clone();

    tokio::spawn(async move {
        let reader = BufReader::new(stdout);
        let mut lines = reader.lines();

        let log_path = "/Users/tedchanglimchangsik/.gemini/antigravity/scratch/mimo_debug_log.txt";
        let _ = tokio::fs::write(log_path, b"=== MIMO STDOUT/STDERR LOG START ===\n").await;

        while let Ok(Some(line)) = lines.next_line().await {
            if let Ok(mut f) = tokio::fs::OpenOptions::new().append(true).open(log_path).await {
                use tokio::io::AsyncWriteExt;
                let _ = f.write_all(format!("[Stdout] {}\n", line).as_bytes()).await;
            }
            if let Ok(response) = serde_json::from_str::<serde_json::Value>(&line) {
                // Handle JSON-RPC response by ID
                if let Some(id) = response.get("id").and_then(|i| i.as_u64()) {
                    if id == 1 {
                        // Response to initialize. Send session/new!
                        let session_new_req = serde_json::json!({
                            "jsonrpc": "2.0",
                            "id": 2,
                            "method": "session/new",
                            "params": {
                                "cwd": "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared",
                                "mcpServers": []
                            }
                        });

                        let mimo_process_init = mimo_process_reader.clone();
                        let mimo_stdin_init = mimo_stdin_reader.clone();
                        let is_connected_init = is_connected_reader.clone();
                        let conversation_id_init = conversation_id_reader.clone();

                        tokio::spawn(async move {
                            let mut stdin_guard = mimo_stdin_init.lock().await;
                            if let Some(ref mut stdin_handle) = *stdin_guard {
                                let session_new_str = format!("{}\n", serde_json::to_string(&session_new_req).unwrap());
                                
                                let write_res = timeout(Duration::from_secs(5), async {
                                    stdin_handle.write_all(session_new_str.as_bytes()).await?;
                                    stdin_handle.flush().await?;
                                    Ok::<(), std::io::Error>(())
                                }).await;
                                
                                if write_res.is_err() || write_res.unwrap().is_err() {
                                    eprintln!("session/new 송신 실패");
                                    drop(stdin_guard);
                                    clean_up_arcs(
                                        mimo_process_init,
                                        mimo_stdin_init,
                                        is_connected_init,
                                        conversation_id_init,
                                    ).await;
                                }
                            }
                        });
                    } else if id == 2 {
                        // Response to session/new. Extract sessionId!
                        if let Some(result) = response.get("result") {
                            if let Some(session_id_str) = result.get("sessionId").and_then(|s| s.as_str()) {
                                let mut conv = conversation_id_clone.lock().await;
                                *conv = Some(session_id_str.to_string());
                                
                                let mut connected = is_connected_clone.lock().await;
                                *connected = true;
                                
                                let _ = app_clone.emit("mimo-connected", session_id_str.to_string());
                            }
                        }
                    } else {
                        // Other request responses (e.g. session/prompt completed)
                        let _ = app_clone.emit("mimo-prompt-done", id);
                    }
                } else {
                    // It is a notification (no id)
                    if let Some(method) = response.get("method").and_then(|m| m.as_str()) {
                        if method == "session/update" {
                            if let Some(params) = response.get("params") {
                                if let Some(update) = params.get("update") {
                                    // Emit raw update to frontend (thought chunks, message chunks, tool calls, etc.)
                                    let _ = app_clone.emit("mimo-update", update.clone());
                                }
                            }
                        }
                    }
                }
            }
        }

        // Reader loop exited - the process has terminated or stdout is closed
        clean_up_arcs(
            mimo_process_reader,
            mimo_stdin_reader,
            is_connected_reader,
            conversation_id_reader,
        ).await;
        let _ = app_clone.emit("mimo-disconnected", "process exited");
    });

    tokio::spawn(async move {
        let reader = BufReader::new(stderr);
        let mut lines = reader.lines();
        let log_path = "/Users/tedchanglimchangsik/.gemini/antigravity/scratch/mimo_debug_log.txt";
        while let Ok(Some(line)) = lines.next_line().await {
            if let Ok(mut f) = tokio::fs::OpenOptions::new().append(true).open(log_path).await {
                use tokio::io::AsyncWriteExt;
                let _ = f.write_all(format!("[Stderr] {}\n", line).as_bytes()).await;
            }
            eprintln!("mimo stderr: {}", line);
        }
    });

    Ok("mimo acp 프로세스 시작 및 initialize 송신 완료".to_string())
}

#[tauri::command]
async fn send_message(
    state: State<'_, AppState>,
    message: String,
    image_data: Option<String>,
) -> Result<String, String> {
    let session_id = {
        let conversation_id = state.conversation_id.lock().await;
        conversation_id.as_ref().ok_or("대화 세션이 존재하지 않습니다")?.clone()
    };

    let mut stdin_guard = state.mimo_stdin.lock().await;
    let stdin = stdin_guard.as_mut().ok_or("MiMo에 연결되지 않았습니다")?;
    
    let mut id = state.request_id.lock().await;
    *id += 1;
    let current_id = *id;
    
    let mut prompt_items = vec![
        serde_json::json!({
            "type": "text",
            "text": message
        })
    ];

    if let Some(ref img_str) = image_data {
        let (media_type, base64_data) = if let Some(comma_pos) = img_str.find(',') {
            let prefix = &img_str[..comma_pos];
            let media_type = if prefix.contains("image/png") {
                "image/png"
            } else if prefix.contains("image/jpeg") || prefix.contains("image/jpg") {
                "image/jpeg"
            } else if prefix.contains("image/gif") {
                "image/gif"
            } else if prefix.contains("image/webp") {
                "image/webp"
            } else {
                "image/png"
            };
            (media_type, &img_str[comma_pos + 1..])
        } else {
            ("image/png", img_str.as_str())
        };

        prompt_items.push(serde_json::json!({
            "type": "image",
            "data": base64_data,
            "mimeType": media_type
        }));
    }

    let request = serde_json::json!({
        "jsonrpc": "2.0",
        "id": current_id,
        "method": "session/prompt",
        "params": {
            "sessionId": session_id,
            "prompt": prompt_items
        }
    });

    use tokio::io::AsyncWriteExt;
    let request_str = format!("{}\n", serde_json::to_string(&request).unwrap());
    
    let write_res = timeout(Duration::from_secs(5), async {
        stdin.write_all(request_str.as_bytes()).await?;
        stdin.flush().await?;
        Ok::<(), std::io::Error>(())
    }).await;

    if write_res.is_err() || write_res.unwrap().is_err() {
        drop(stdin_guard);
        clean_up_arcs(
            state.mimo_process.clone(),
            state.mimo_stdin.clone(),
            state.is_connected.clone(),
            state.conversation_id.clone(),
        ).await;
        return Err("메시지 전송 실패 (시간 초과 또는 파이프 오류)".to_string());
    }

    Ok(current_id.to_string())
}

#[tauri::command]
async fn cancel_generation(state: State<'_, AppState>) -> Result<String, String> {
    let session_id = {
        let conversation_id = state.conversation_id.lock().await;
        conversation_id.as_ref().ok_or("대화 세션이 존재하지 않습니다")?.clone()
    };

    let mut stdin_guard = state.mimo_stdin.lock().await;
    let stdin = stdin_guard.as_mut().ok_or("MiMo에 연결되지 않았습니다")?;
    
    let request = serde_json::json!({
        "jsonrpc": "2.0",
        "method": "session/cancel",
        "params": {
            "sessionId": session_id
        }
    });

    use tokio::io::AsyncWriteExt;
    let request_str = format!("{}\n", serde_json::to_string(&request).unwrap());
    
    let write_res = timeout(Duration::from_secs(5), async {
        stdin.write_all(request_str.as_bytes()).await?;
        stdin.flush().await?;
        Ok::<(), std::io::Error>(())
    }).await;

    if write_res.is_err() || write_res.unwrap().is_err() {
        drop(stdin_guard);
        clean_up_arcs(
            state.mimo_process.clone(),
            state.mimo_stdin.clone(),
            state.is_connected.clone(),
            state.conversation_id.clone(),
        ).await;
        return Err("취소 요청 전송 실패 (시간 초과 또는 파이프 오류)".to_string());
    }

    Ok("취소 요청됨".to_string())
}

#[tauri::command]
async fn disconnect_mimo(state: State<'_, AppState>) -> Result<String, String> {
    clean_up_arcs(
        state.mimo_process.clone(),
        state.mimo_stdin.clone(),
        state.is_connected.clone(),
        state.conversation_id.clone(),
    ).await;

    Ok("MiMo 연결 해제됨".to_string())
}

#[tauri::command]
async fn get_connection_status(state: State<'_, AppState>) -> Result<bool, String> {
    let is_connected = state.is_connected.lock().await;
    Ok(*is_connected)
}

#[tauri::command]
async fn create_new_conversation(
    state: State<'_, AppState>,
) -> Result<String, String> {
    let mut stdin_guard = state.mimo_stdin.lock().await;
    let stdin = stdin_guard.as_mut().ok_or("MiMo에 연결되지 않았습니다")?;
    
    let mut id = state.request_id.lock().await;
    *id += 1;
    let current_id = *id;

    let request = serde_json::json!({
        "jsonrpc": "2.0",
        "id": current_id,
        "method": "session/new",
        "params": {
            "cwd": "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared",
            "mcpServers": []
        }
    });

    use tokio::io::AsyncWriteExt;
    let request_str = format!("{}\n", serde_json::to_string(&request).unwrap());
    
    let write_res = timeout(Duration::from_secs(5), async {
        stdin.write_all(request_str.as_bytes()).await?;
        stdin.flush().await?;
        Ok::<(), std::io::Error>(())
    }).await;

    if write_res.is_err() || write_res.unwrap().is_err() {
        drop(stdin_guard);
        clean_up_arcs(
            state.mimo_process.clone(),
            state.mimo_stdin.clone(),
            state.is_connected.clone(),
            state.conversation_id.clone(),
        ).await;
        return Err("새 대화 생성 요청 실패 (시간 초과 또는 파이프 오류)".to_string());
    }

    Ok("새 대화 생성 요청됨".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(AppState::new())
        .invoke_handler(tauri::generate_handler![
            connect_mimo,
            send_message,
            disconnect_mimo,
            get_connection_status,
            create_new_conversation,
            cancel_generation
        ])
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                let app_state = window.state::<AppState>();
                let mimo_process = app_state.mimo_process.clone();
                tauri::async_runtime::spawn(async move {
                    let mut process = mimo_process.lock().await;
                    if let Some(mut child) = process.take() {
                        let _ = child.kill().await;
                        println!("mimo acp 자식 프로세스 안전 종료됨");
                    }
                });
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
