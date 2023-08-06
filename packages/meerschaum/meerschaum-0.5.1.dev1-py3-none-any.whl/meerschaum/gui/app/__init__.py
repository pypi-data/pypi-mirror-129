#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Define the `toga.App` implementation here.
"""

from __future__ import annotations
from meerschaum.utils.typing import Optional, List, Dict, Any

from meerschaum.utils.packages import attempt_import
toga = attempt_import('toga', lazy=False, venv=None)

class MeerschaumApp(toga.App):

    from meerschaum.gui.app._windows import get_main_window
    from meerschaum.gui.app.pipes import build_pipes_tree, _pipes_tree_on_select_handler
    from meerschaum.gui.app.actions import add_actions_as_commands

    def __init__(
        self,
        *args: Any,
        mrsm_instance: Optional[str] = None,
        debug: bool = False,
        **kw: Any
    ):
        """
        Set the initial state of the GUI application from the keyword arguments.
        """
        from meerschaum.utils.misc import filter_keywords
        _init = super(MeerschaumApp, self).__init__
        _init(*args, **filter_keywords(_init, **kw))
        self._debug = debug
        self._windows = {}
        self._instance = mrsm_instance
        self._kw = kw

    def startup(self) -> None:
        """
        Entrypoint for the GUI application.
        """
        self.main_window = self.get_main_window()
        self.main_window.show()
