from pathlib import Path


def format_report(path_a: Path, path_b: Path, results: dict) -> str:
    lines = []
    lines.append(
        f"\nComparing: {path_a.name} ({results['len_a']} pages)"
        f" vs {path_b.name} ({results['len_b']} pages)\n"
    )

    has_diffs = results["changed"] or results["added"] or results["removed"]

    if not has_diffs:
        lines.append("No differences found. All pages are identical.\n")
    else:
        lines.append("DIFFERENT pages:")
        for page_num, ratio in results["changed"]:
            lines.append(f"  Page {page_num:>4}  — similarity: {ratio * 100:.1f}%")
        if results["removed"]:
            for page_num in results["removed"]:
                lines.append(f"  Page {page_num:>4}  — only in {path_a.name}")
        if (results["added"]):
            for page_num in results["added"]:
                lines.append(f"  Page {page_num:>4}  — only in {path_b.name}")
        lines.append("")

    lines.append(
        f"Summary: {len(results['changed'])} changed, "
        f"{len(results['added'])} added, "
        f"{len(results['removed'])} removed, "
        f"{results['identical']} identical"
    )
    return "\n".join(lines)
