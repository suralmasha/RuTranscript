from pydantic import BaseModel


class PosttonicAllophones(BaseModel):
    """Allophones for posttonic phonemes in different positions."""

    after_hissing: str | None = None
    after_hard: str | None = None
    after_others: str | None = None


class FirstPretonicAllophones(BaseModel):
    """Allophones for first pretonic phonemes in different positions."""

    after_hissing: str | None = None
    after_zh_sh_ts: str | None = None
    after_hard: str | None = None
    after_others: str | None = None
