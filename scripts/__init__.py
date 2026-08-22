"""Package-level registrations shared by repository tools and tests."""

from . import info_stories as info_stories

# Narrative taste is intentionally a separate retrieval projection. It carries
# story progression and originality cues without leaking layout or motion payloads.
info_stories.CAPSULE_FIELDS.setdefault(
    "narrative",
    (
        "story_jobs",
        "hook",
        "beats",
        "hierarchy",
        "originality",
        "anti_patterns",
        "reference_ids",
    ),
)
