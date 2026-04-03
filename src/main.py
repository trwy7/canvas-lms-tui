import pip_system_certs.wrapt_requests # PYInstaller
pip_system_certs.wrapt_requests.inject_truststore() # PYInstaller
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
import json
import requests
import src.saves

class CanvasTUI(App):
    """A TUI for Canvas."""

    BINDINGS = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        MODES = {} # TODO: Add 
        #yield Footer()


if __name__ == "__main__":
    app = CanvasTUI()
    app.run()