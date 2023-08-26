from jira import JIRA
from const import USERNAME, PASSWORD, SERVER
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter

# Connect Jira
jira_connector = JIRA(
    basic_auth=(USERNAME, PASSWORD),
    options={"server": SERVER},
)

# Get support tickets words
support_epic = "PLAT-362"
jql = f'"Epic Link" = {support_epic}'
issues = jira_connector.search_issues(jql, maxResults=500)
all_words = []

# Create list of words based
## Occurrence of each word is based on the estimate of the ticket
for issue in issues:
    estimate = float(issue.fields.customfield_10106)
    estimate_bucket = estimate / 0.5
    issue_words = issue.fields.summary.split()

    cleaned_words = [re.sub(r"[^a-zA-Z]", "", word).lower() for word in issue_words]
    duplicated_words = [
        word for word in cleaned_words for _ in range(int(estimate_bucket))
    ]
    all_words.extend(duplicated_words)

# Count word occurrences
word_counts = Counter(all_words)

# Clean the data
filter_words = [
    "issue",
    "issues",
    "test",
    "on",
    "for",
    "in",
    "to",
    "minor",
    "new",
    "use",
    "v",
    "v4",
    "epic",
    "not",
    "and",
]
for filter_word in filter_words:
    word_counts.pop(filter_word, None)

# Create Word Cloud
wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(word_counts)
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("support_wordcloud.png", bbox_inches="tight")
plt.show()
