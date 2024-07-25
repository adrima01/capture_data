import argparse
from similarius import get_website, extract_text_ressource, sk_similarity, ressource_difference, ratio

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--website", nargs="+", help="Website to compare")
parser.add_argument("-o", "--original", help="Website to compare")
args = parser.parse_args()

# Original
original = get_website(args.original)

if not original:
    print("[-] The original website is unreachable...")
    exit(1)

original_text, original_ressource = extract_text_ressource(original.text)

for website in args.website:
    print(f"\n********** {args.original} <-> {website} **********")

    # Compare
    compare = get_website(website)

    if not compare:
        print(f"[-] {website} is unreachable...")
        continue

    compare_text, compare_ressource = extract_text_ressource(compare.text)

    # Calculate
    sim = str(sk_similarity(compare_text, original_text))
    print(f"\nSimilarity: {sim}")

    ressource_diff = ressource_difference(original_ressource, compare_ressource)
    print(f"Ressource Difference: {ressource_diff}")

    ratio_compare = ratio(ressource_diff, sim)
    print(f"Ratio: {ratio_compare}")