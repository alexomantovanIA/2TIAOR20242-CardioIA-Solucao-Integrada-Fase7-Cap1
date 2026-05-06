"""
CardioIA Fase 6 — agents package.

Re-exports openai-agents SDK symbols (Agent, Runner, handoff, function_tool)
to resolve the naming conflict between this local package and the installed SDK.
"""
import os
import sys
from pathlib import Path

_LOCAL = os.path.realpath(str(Path(__file__).parent))
_PARENT = os.path.realpath(str(Path(__file__).parent.parent))

# Find the SDK's 'agents' directory in site-packages
_sdk_dir = None
for _p in sys.path:
    if "site-packages" in _p:
        _d = os.path.join(_p, "agents")
        if os.path.isdir(_d) and os.path.realpath(_d) != _LOCAL:
            _sdk_dir = _d
            break

if _sdk_dir:
    # Temporarily remove local project root from sys.path so 'import agents'
    # resolves to the SDK in site-packages instead of this local package.
    _saved_path = list(sys.path)
    sys.path[:] = [
        p for p in sys.path
        if os.path.realpath(p) not in (_PARENT, _LOCAL) and p != ""
    ]

    # Remove this partial module from sys.modules so Python re-imports fresh
    _partial = sys.modules.pop("agents", None)
    _sdk_submods = {}

    try:
        import agents as _sdk  # imports from site-packages

        # Collect SDK exports we need
        Agent = getattr(_sdk, "Agent", None)
        Runner = getattr(_sdk, "Runner", None)
        handoff = getattr(_sdk, "handoff", None)
        function_tool = getattr(_sdk, "function_tool", None)

        # Stash SDK submodule entries so they remain usable by SDK classes
        _sdk_submods = {
            k: v for k, v in sys.modules.items()
            if k.startswith("agents.") and not k.startswith("agents.tools")
            and not k.startswith("agents.tests") and k != "agents.config"
        }

    except Exception:
        Agent = Runner = handoff = function_tool = None
    finally:
        # Restore sys.path
        sys.path[:] = _saved_path
        # Restore this local package in sys.modules
        if _partial is not None:
            sys.modules["agents"] = _partial
        # Preserve SDK submodule entries (needed by SDK internals at runtime)
        for _k, _v in _sdk_submods.items():
            sys.modules.setdefault(_k, _v)
