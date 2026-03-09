from typing import Optional

from .embed import build_embed, format_metrics
from .webhook import DiscordWebhook


class TrainNotifier:
    def __init__(self, webhook_url: str, username: str = "Train Logger", timeout: int = 10):
        self._webhook = DiscordWebhook(webhook_url, timeout=timeout)
        self._username = username

    def _post(self, embeds: list, content: str = "") -> bool:
        payload: dict = {"username": self._username, "embeds": embeds}
        if content:
            payload["content"] = content
        return self._webhook.send(payload)

    def _post_with_file(self, embeds: list, file_path: str, filename: Optional[str] = None) -> bool:
        payload: dict = {"username": self._username, "embeds": embeds}
        return self._webhook.send_with_file(payload, file_path, filename)

    def on_train_start(self, experiment: str, config_summary: Optional[dict] = None) -> bool:
        fields = {"Experiment": experiment}
        if config_summary:
            fields.update(config_summary)

        embed = build_embed(
            title="Training Started",
            color="green",
            fields=fields,
        )
        return self._post([embed])

    def on_epoch_end(
        self,
        epoch: int,
        metrics: dict,
        total_epochs: Optional[int] = None,
        step: Optional[int] = None,
    ) -> bool:
        title = f"Epoch {epoch}"
        if total_epochs:
            title += f" / {total_epochs}"

        description = f"Step {step}" if step is not None else ""

        embed = build_embed(
            title=title,
            description=description,
            color="blue",
            fields=format_metrics(metrics),
        )
        return self._post([embed])

    def on_checkpoint_saved(self, step: int, path: str) -> bool:
        embed = build_embed(
            title="Checkpoint Saved",
            color="gray",
            fields={"Step": str(step), "Path": f"`{path}`"},
        )
        return self._post([embed])

    def on_train_end(
        self,
        total_steps: int,
        best_val_loss: Optional[float] = None,
    ) -> bool:
        fields: dict = {"Total Steps": str(total_steps)}
        if best_val_loss is not None:
            fields["Best Val Loss"] = f"{best_val_loss:.4f}"

        embed = build_embed(
            title="Training Complete",
            color="green",
            fields=fields,
        )
        return self._post([embed])

    def on_error(self, error: Exception, context: str = "") -> bool:
        description = f"```{type(error).__name__}: {error}```"
        if context:
            description = f"**Context:** {context}\n{description}"

        embed = build_embed(
            title="Training Error",
            description=description,
            color="red",
        )
        return self._post([embed])

    def send(self, message: str, color: str = "blue") -> bool:
        embed = build_embed(title=message, color=color)
        return self._post([embed])

    def send_file(self, file_path: str, message: str = "", filename: Optional[str] = None) -> bool:
        embeds = []
        if message:
            embeds.append(build_embed(title=message, color="blue"))
        return self._post_with_file(embeds, file_path, filename)
