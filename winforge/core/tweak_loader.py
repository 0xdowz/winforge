import json
import logging
from pathlib import Path
from typing import List

from winforge.models.tweak import Tweak
from winforge.utils.paths import get_config_dir

logger = logging.getLogger("winforge")


def load_tier1_tweaks() -> List[Tweak]:
    """Loads Tier 1 safe tweaks from config/tweaks/*.json files."""
    tweaks: List[Tweak] = []
    cfg_dir = get_config_dir()
    tweaks_dir = cfg_dir / "tweaks"

    if not tweaks_dir.exists():
        logger.warning(f"Tweaks directory not found at {tweaks_dir}")
        return []

    for json_file in tweaks_dir.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        tweak = Tweak.model_validate(item)
                        tweaks.append(tweak)
        except Exception as e:
            logger.error(f"Failed loading tweaks from {json_file.name}: {e}")

    logger.info(f"Loaded {len(tweaks)} Tier 1 safe tweaks from database.")
    return tweaks
