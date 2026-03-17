from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, custom_prompt: str | None = None):
    """Generate a post. If `custom_prompt` is provided (non-empty), use it
    as the base prompt and append few-shot examples when available.
    """
    if custom_prompt and custom_prompt.strip():
        prompt = custom_prompt
        examples = few_shot.get_filtered_posts(length, language, tag)
        if len(examples) > 0:
            prompt += "\n\n4) Use the writing style as per the following examples."
            for i, post in enumerate(examples):
                post_text = post.get('text', '')
                prompt += f'\n\n Example {i+1}: \n\n {post_text}'
                if i == 1:  # Use max two samples
                    break
    else:
        prompt = get_prompt(length, language, tag)

    prompt = _sanitize_text(prompt)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


def _sanitize_text(s: str) -> str:
    """Remove Unicode surrogate code units which cause UTF-8 encoding errors.

    Surrogate halves (U+D800..U+DFFF) may appear in malformed JSON or from
    certain emoji encodings; remove them before sending to the API.
    """
    if not isinstance(s, str):
        return s
    return "".join(ch for ch in s if not (0xD800 <= ord(ch) <= 0xDFFF))


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))