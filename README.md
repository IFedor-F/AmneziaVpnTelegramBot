# Amnezia WG Config Generator Bot

This Telegram bot helps the admin of a VPS easily generate a QR code and configuration file for Amnezia WireGuard (AWG) networks. The bot automates the process of adding new peers to a specific AWG network and sends the necessary configuration data to users in various formats (QR code, plain text, and `.conf` file).

## Features

- Only authorized Telegram users (based on their Telegram ID) can use the bot.
- The bot generates a new peer configuration for an AWG network when the `/generate [awg_network_name] [comment]` command is issued.
- It updates the respective AWG configuration file (`awg_network_name.conf`) with the new peer and then sends the user their configuration details in multiple formats:
  - **QR code** for easy scanning and import.
  - **Plain text** message with the configuration details.
  - **`.conf` file** (`awg_userconfig.conf`) for manual use.

### Example Peer Entry in `awg_network_name.conf`:

```
# comment 
[Peer]
PublicKey = <Generated Public Key>
AllowedIPs = <Next Available IP (e.g., 192.168.12.3/32)>
```

## Installation

### Requirements

1. **Telegram Bot API Token**: Obtain this from [BotFather](https://t.me/BotFather) and store it in an environment variable.
2. **AWG Configuration Files**: Ensure you have AWG network configuration files available on your VPS, such as `/etc/amnezia/amneziawg/awg0.conf`.

### Configuration Files

#### 1. `config.json` - VPN Configuration

This file holds the configuration for each AWG network the bot manages.

Example:
```json
{
  "awg0": {
    "path_to_config": "/etc/amnezia/amneziawg/awg0.conf",
    "restart_command": "awg-quick down awg0; awg-quick up awg0"
  },
  "awg1": {
    "path_to_config": "/etc/amnezia/amneziawg/awg1.conf",
    "restart_command": "awg-quick down awg1; awg-quick up awg1"
  }
}
```

- **`path_to_config`**: Path to the configuration file for the specific AWG network.
- **`restart_command`**: Command to restart the AWG network after adding a new peer.

#### 2. `tg_config.json` - Telegram Configuration

This file defines the bot’s Telegram settings.

Example:
```json
{
  "admin_ids": [123456789],
  "API_TOKEN_ENV_NAME": "TELEGRAM_API_TOKEN"
}
```

- **`admin_ids`**: List of Telegram user IDs who are authorized to use the bot's commands.
- **`API_TOKEN_ENV_NAME`**: The environment variable name where your Telegram bot token is stored.

#### 3. `awg0.pattern` - AWG User Config Template

This is the template for user configurations that the bot generates. You can customize this for each AWG network in the `user_config_awg_patterns/` directory. 

Example (`awg0.pattern`):
```
[Interface]
PrivateKey = $private_key
ListenPort = 51820
Address = $client_local_ip
MTU = 1420

[Peer]
PublicKey = <Server Public Key>
AllowedIPs = 0.0.0.0/1, 128.0.0.0/1
Endpoint = <Server IP>:<Server Port>
PersistentKeepalive = 20
```

- **Variables**:
  - `$private_key`: Generated private key for the peer.
  - `$client_local_ip`: The next available IP address for the peer.

You can create a separate pattern file for each AWG network (e.g., `awg1.pattern`).

## Usage

### Command

- **`/generate [awg_network_name] [comment]`**

  This command is available only to users whose Telegram IDs are listed in the `admin_ids` array in the `tg_config.json` file.

- **Example**:
  ```
  /generate awg0 New User Connection
  ```

### Bot Actions

1. The bot generates a new peer entry in the specified AWG configuration file (`awg_network_name.conf`).
   
2. The bot assigns the next available IP address to the new peer (e.g., `192.168.12.3/32`).

3. The bot sends the user their configuration in three formats:
   - **QR code** for easy import.
   - **Plain text** configuration details.
   - **`.conf` file** (`awg_userconfig.conf`) for manual configuration.

4. The AWG network is restarted using the `restart_command` specified in `config.json`.

## Environment Setup

Ensure the following environment variables are set:

- **Telegram Bot Token**: The bot retrieves its token from an environment variable defined in `tg_config.json` (`API_TOKEN_ENV_NAME`).
  
Example (Linux):
```bash
export TELEGRAM_FRACTAL_API_TOKEN=your_telegram_bot_token_here
```