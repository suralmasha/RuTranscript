from __future__ import annotations

from importlib.resources import files

import pandas as pd
import panphon.featuretable
from panphon.segment import Segment


def patch_panphon_resource_encoding() -> None:
    """Read panphon CSV resources as UTF-8 regardless of the process locale."""
    if getattr(panphon.featuretable.FeatureTable, '_ru_transcript_utf8_patch', False):
        return

    def _read_bases(
        _self: panphon.featuretable.FeatureTable, fn: str, weights: list[float]
    ) -> tuple[list[tuple[str, Segment]], dict[str, Segment], list[str]]:
        spec_to_int = {'+': 1, '0': 0, '-': -1}

        with files('panphon').joinpath(fn).open(encoding='utf-8') as f:
            df = pd.read_csv(f)

        df['ipa'] = df['ipa'].apply(_self.normalize)

        feature_names = list(df.columns[1:])
        df[feature_names] = df[feature_names].map(lambda x: spec_to_int[x])
        segments = [
            (row['ipa'], Segment(feature_names, row[1:].to_dict(), weights=weights)) for (_, row) in df.iterrows()
        ]
        seg_dict = dict(segments)

        return segments, seg_dict, feature_names

    def _read_weights(_self: panphon.featuretable.FeatureTable, weights_fn: str) -> list[float]:
        with files('panphon').joinpath(weights_fn).open(encoding='utf-8') as f:
            df = pd.read_csv(f)
        return df.iloc[0].astype(float).tolist()

    panphon.featuretable.FeatureTable._read_bases = _read_bases  # noqa: SLF001
    panphon.featuretable.FeatureTable._read_weights = _read_weights  # noqa: SLF001
    panphon.featuretable.FeatureTable._ru_transcript_utf8_patch = True  # noqa: SLF001
