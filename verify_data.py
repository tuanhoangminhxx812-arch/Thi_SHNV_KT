import sys, json
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('data.json', 'r', encoding='utf-8'))
vp = data.get('Khối VP', {})
print(f"Khối VP has {len(vp)} topics:")
for k, v in vp.items():
    print(f"  {k}: {len(v)} questions")
    q = v[0]
    print(f"    Keys: {list(q.keys())}")
    print(f"    Q: {q['question'][:80]}")
    print(f"    Answers ({len(q['answers'])}): {[a[:40] for a in q['answers']]}")
    print(f"    correct_idx: {q['correct_idx']}")
    # Check for any bad questions
    bad = [i for i, qq in enumerate(v) if qq['correct_idx'] < 0 or qq['correct_idx'] >= len(qq['answers']) or not qq['answers']]
    if bad:
        print(f"    ⚠️ BAD questions at indices: {bad}")
    else:
        print(f"    ✅ All questions valid")
