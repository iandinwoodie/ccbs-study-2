#!/usr/bin/env python3

import pandas as pd
import sys


TRAIT_COLS = [
    'appearance',
    'breed',
    'size',
    'age',
    'personality',
    'trainability',
    'compatibility'
]


def add_rank_cols(df):
    for col in TRAIT_COLS:
        df[col] = 0
    rank_cols = [
        'MostImp1_Rec',
        'MostImp2_Rec',
        'MostImp3_Rec',
        'MostImp4_Rec',
        'MostImp5_Rec',
        'MostImp6_Rec'
    ]
    reference_set = set(range(0, 6+1))

    def rank_response(row):
        response_set = set()
        rank_value = 1
        for rank_col in rank_cols:
            trait_idx = row[rank_col] - 1
            trait_col = TRAIT_COLS[trait_idx]
            response_set.add(trait_idx)
            row[trait_col] = rank_value
            rank_value += 1
        trait_idx = list(reference_set - response_set)[0]
        trait_col = TRAIT_COLS[trait_idx]
        row[trait_col] = rank_value
        return row

    return df.apply(rank_response, axis=1)


def add_rank_sum_col(df):
    df['rank_sum'] = df[TRAIT_COLS].sum(axis=1)
    return df


def main():
    if len(sys.argv) != 3:
        print('Usage: rank.py <input-csv> <output-csv>')
        sys.exit(1)
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    df = pd.read_csv(input_csv)
    df = add_rank_cols(df)
    df = add_rank_sum_col(df)
    df.to_csv(output_csv, index=False)
    print(df)


if __name__ == '__main__':
    main()
