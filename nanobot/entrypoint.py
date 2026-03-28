#!/usr/bin/env python3
"""
Nanobot gateway entrypoint.

Resolves environment variables into config.json at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    app_dir = Path("/app")
    config_path = app_dir / "config.json"
    resolved_config_path = app_dir / "config.resolved.json"
    workspace_dir = app_dir / "workspace"

    # Read base config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Override with environment variables
    # LLM provider
    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key

    if llm_api_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base

    if llm_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_model

    # Gateway
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    # Webchat channel
    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        config["channels"]["webchat"] = {
            "enabled": True,
            "host": webchat_host,
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", 8765)),
            "allowFrom": ["*"],
        }
        # Pass access key to webchat channel
        if access_key := os.environ.get("NANOBOT_ACCESS_KEY"):
            config["channels"]["webchat"]["accessToken"] = access_key

    # Webchat MCP server
    if ui_relay_url := os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_URL"):
        if "tools" not in config:
            config["tools"] = {}
        if "mcpServers" not in config["tools"]:
            config["tools"]["mcpServers"] = {}
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_WEBCHAT_UI_RELAY_URL": ui_relay_url,
                "NANOBOT_WEBCHAT_UI_RELAY_TOKEN": os.environ.get(
                    "NANOBOT_WEBCHAT_UI_RELAY_TOKEN", "webchat-secret"
                ),
            },
        }

    # MCP LMS server environment
    if "tools" not in config:
        config["tools"] = {}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}

    if "lms" in config["tools"]["mcpServers"]:
        lms_config = config["tools"]["mcpServers"]["lms"]
        if "env" not in lms_config:
            lms_config["env"] = {}

        if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
            lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url

        if backend_api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
            lms_config["env"]["NANOBOT_LMS_API_KEY"] = backend_api_key

    # MCP Observability server environment
    if "obs" in config["tools"]["mcpServers"]:
        obs_config = config["tools"]["mcpServers"]["obs"]
        if "env" not in obs_config:
            obs_config["env"] = {}

        if victorialogs_url := os.environ.get("NANOBOT_VICTORIALOGS_URL"):
            obs_config["env"]["NANOBOT_VICTORIALOGS_URL"] = victorialogs_url

        if victoriatraces_url := os.environ.get("NANOBOT_VICTORIATRACES_URL"):
            obs_config["env"]["NANOBOT_VICTORIATRACES_URL"] = victoriatraces_url

    # Write resolved config
    with open(resolved_config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_config_path}", file=sys.stderr)

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_config_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
