import logging
from importlib import import_module
from pathlib import Path
from aiogram import Dispatcher

logger = logging.getLogger(__name__)

routers = []

package_dir = Path(__file__).parent
for path in package_dir.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    relative_path = path.relative_to(package_dir.parent)
    module_parts = relative_path.with_suffix("").parts
    module_name = ".".join(module_parts)

    module = import_module(f".{module_name}", package="app")
    router = getattr(module, "router", None)
    if not router:
        logger.warning(f"No 'router' variable found in {module_name}")
    routers.append(router)


def setup(dp: Dispatcher):
    """Setups all routers"""
    for router in routers:
        dp.include_router(router)
