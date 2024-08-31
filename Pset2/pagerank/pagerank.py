import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # Calculate the transition probabilities
    n_pages = len(corpus)
    probs = dict.fromkeys(corpus.keys(), (1 - damping_factor) / n_pages)
    links = corpus[page]

    if links:
        for l in links:
            probs[l] += damping_factor / len(links)
    else:
        for p in probs:
            probs[p] += damping_factor / n_pages

    return probs 

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Simulate the random surfer for a large number of iterations
    pr = dict.fromkeys((corpus), 0)
    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pr[page] += 1
        probs = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probs.keys()), weights=probs.values(), k=1)[0]

    for page in pr:
        pr[page] /= n

    return pr    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Update the PageRank values iteratively until they converge.
    n_pages = len(corpus)
    pr = dict.fromkeys(corpus.keys(), 1 / n_pages)

    # Define a convergence treshold
    c_threshold = 0.001
    converged = False 

    while not converged:
        new_rank = {}
        converged = True

        for page in pr:
            # Calculate the rank for this page
            rank = (1 - damping_factor) / n_pages

            for p in corpus:
                if page in corpus[p]:
                    rank += damping_factor * pr[p] / len(corpus[p])
                
                if not corpus[p]:  # Handle pages with no links
                    rank += damping_factor * pr[p] / n_pages
            
            new_rank[page] = rank

        # Check if the change is larger than the threshold
        for page in pr:
            if abs(new_rank[page] - pr[page]) > c_threshold:
                converged = False

        pr = new_rank

        # Debug: Print the current PageRank values
        print("Current PageRank values:")
        for page in pr:
            print(f"  {page}: {pr[page]:.4f}")

    return pr

if __name__ == "__main__":
    main()
