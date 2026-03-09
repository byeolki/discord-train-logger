# discord-train-logger

Discord webhook notifications for ML training jobs.

## Installation

```bash
pip install discord-train-logger
```

## Quick Start

```python
from discord_train_logger import TrainNotifier

notifier = TrainNotifier(webhook_url="https://discord.com/api/webhooks/...")

# Training lifecycle
notifier.on_train_start(
    experiment="my-experiment",
    config_summary={"epochs": 1000, "batch_size": 32}
)

notifier.on_epoch_end(
    epoch=5,
    metrics={"loss_g": 0.42, "val_loss": 0.38},
    total_epochs=1000,
    step=5000,
)

notifier.on_checkpoint_saved(step=5000, path="/checkpoints/step_5000.pt")

notifier.on_train_end(total_steps=50000, best_val_loss=0.31)

# Error handling
try:
    ...
except Exception as e:
    notifier.on_error(e, context="train_step")

# Send audio/image samples
notifier.send_file("sample.wav", message="Validation sample @ step 5000")

# Custom message
notifier.send("Preemption detected, saving checkpoint...", color="yellow")
```

## Getting a Webhook URL

1. Go to your Discord server settings
2. Integrations → Webhooks → New Webhook
3. Copy the webhook URL

## API

### `TrainNotifier(webhook_url, username="Train Logger", timeout=10)`

| Method | Description |
|--------|-------------|
| `on_train_start(experiment, config_summary)` | Notify training started |
| `on_epoch_end(epoch, metrics, total_epochs, step)` | Notify epoch completion with metrics |
| `on_checkpoint_saved(step, path)` | Notify checkpoint saved |
| `on_train_end(total_steps, best_val_loss)` | Notify training complete |
| `on_error(error, context)` | Notify training error |
| `send(message, color)` | Send a custom message |
| `send_file(file_path, message, filename)` | Send a file attachment |

Available colors: `green`, `red`, `yellow`, `blue`, `gray`, `orange`

## License

MIT
