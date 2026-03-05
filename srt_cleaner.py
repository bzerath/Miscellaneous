from pathlib import Path
from itertools import islice


root = Path("G:/Nouveaudossier")

srts = list(root.glob("*.srt"))

for srt in srts:
    if "Copie" in srt.name or "_reworked" in srt.name:
        continue
    new_name = srt.with_name(srt.stem + "_reworked" + srt.suffix)
    print(srt, "-->", new_name)
    soustitres_bruts: list[tuple[str, str]] = []
    with open(srt, "r", encoding="utf-8") as f:
        while groupe := list(islice(f, 4)):
            soustitres_bruts.append((groupe[1].strip(), groupe[2].strip()))


    with open(new_name, "w", encoding="utf-8") as f:
        for i, (timestamp, texte) in enumerate(soustitres_bruts):
            f.write(f"{i+1}\n")
            f.write(f"{timestamp}\n")
            f.write(f"{texte}\n")
            f.write("\n")