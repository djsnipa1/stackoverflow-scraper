from SoupKitchen.Utensils import MakeSoup
import string

def remove_non_ascii(str):
    """
    Remove any non-ascii characters to prevent errors
    """

    return ''.join(filter(lambda x: x in string.printable, str))


def replace_with_md(tag, block, start, end, alt_start='', alt_end=''):
    """
    Replace html tags with markdown
    """

    for tag_item in block.find_all(tag):
        tag_item_len = len(tag_item.text)

        if (tag_item.parent.name == "pre"):
            tag_item.insert(0, alt_start)
            tag_item.insert(tag_item_len, alt_end)
        else:
            tag_item.insert(0, start)
            tag_item.insert(tag_item_len, end)

    return block


def write_item_head(file_handle, header, link, vote_count, user_name):
    """
    Write the name of the post with a link, and the number of votes it has
    """
    user_name = remove_non_ascii(user_name)

    file_handle.write("\n## [" + header + "](" + link  + ")\n\n")
    file_handle.write("**" + vote_count + " Votes**, " + user_name + "\n\n")


def to_markdown(link, file_handle):
    """
    Delve into link and scrape the text of the first answer, then write to file
    """

    sub_page = MakeSoup(link)

    post = sub_page.find("div", {"itemprop": "acceptedAnswer"})

    if not post:
        post = sub_page.find("div", {"class": "answer"})

    answer = post.find("div", {"class": "post-text"})

    answer = replace_with_md("code", answer, "`", "`", "\n```python\n", "```\n")
    answer = replace_with_md("h2", answer, "\n### ", "\n")

    file_handle.write(remove_non_ascii(answer.text.strip()))


topic = "Javascript"  #Topic to search for, also in title
page_size = 50       #Number of posts to scrape
base_url = "https://stackoverflow.com"

doc_title = "StackOverflow Top " + topic + " Questions"
output_location = "../output/"                                #Choose output directory
file_name = doc_title.replace(' ', '_')                       #No whitespace for title
file_type = ".md"

links = []
titles = []
votes = []

f = open(output_location + file_name + file_type, 'w')

f.write("# " + doc_title + "\n\n")

soup = MakeSoup("https://stackoverflow.com/questions/tagged/"
                + topic.lower() +
                "?sort=votes&pageSize="
                + str(page_size))

main_div = soup.find(id="questions")

question_divs = main_div.find_all("div", {"class": "question-summary"})

for div, count in zip(question_divs, range(0, len(question_divs))):
    heading = div.find("h3")
    anchor = heading.find("a")
    question_vote = div.find("span", {"class": "vote-count-post"})
    user_details = div.find("div", {"class": "user-details"})

    title = remove_non_ascii(anchor.text.strip())
    link = base_url + anchor["href"]
    vote = question_vote.text.strip()

    user = user_details.find("a")

    if user:
        user = user_details.find("a").text.strip()
    elif user_details.find("span"): 
        user = user_details.find("span")["class"][0]
    else:
        user = user_details.text

    # titles.append(title)
    # links.append(anchor["href"])
    # votes.append(question_vote.text.strip())

    print("Output [" + str(count) + "]: " + title)
    write_item_head(f, title, link, vote, user)
    to_markdown(link, f)
    f.write("\n")

f.close()