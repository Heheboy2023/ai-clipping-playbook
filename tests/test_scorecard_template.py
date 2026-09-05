from clipkit.candidates import score_candidates


def test_documented_scorecard_matches_cli(repository_root, tmp_path):
    result = score_candidates(repository_root / 'templates/moment-scorecard.csv',
                              tmp_path / 'scored.csv')
    assert result['candidates'] == 1
    assert result['eligible'] == 0
    assert result['disqualified'] == 1
    assert result['performance_prediction'] is False
