import argparse
from similarius import get_website, extract_text_ressource, sk_similarity, ressource_difference, ratio


# Original
original = "www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F-%2Fen%2Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"  # Beispiel-URL für die Original-Website
websites_to_compare = ["https://vitalesante-renouvellement.com/pages/index.php"]  # Liste der zu vergleichenden Websites

# Original
original = get_website(original)

if not original:
    print("[-] The original website is unreachable...")
    exit(1)

original_text, original_ressource = extract_text_ressource(original.text)

for website in websites_to_compare:
    print(f"\n********** {original} <-> {website} **********")

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

"""
Beispiel
python3 similarius_test.py -o paypal.com/signin -w main.d1rqan5j5td705.amplifyapp.com/otp3.html
"""