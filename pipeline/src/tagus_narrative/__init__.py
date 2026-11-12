"""Offline narrative pipeline for the Tagus sailing game.

Stages: ingest -> index -> retrieve -> generate -> verify -> review -> export.
Only the line-record validator is implemented so far (see validate.py).
"""

__version__ = "0.1.0"
