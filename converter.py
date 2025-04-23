import os
from bs4 import BeautifulSoup

def convert_html_to_txt(html_filepath, txt_filepath=None, return_content=False):
    """
    Reads an HTML file, extracts the text content.
    Optionally saves it to a TXT file or returns the content.

    Args:
        html_filepath (str): The path to the input HTML file.
        txt_filepath (str, optional): The path where the output TXT file will be saved.
                                     Required if return_content is False. Defaults to None.
        return_content (bool, optional): If True, returns the extracted text content
                                         instead of writing to a file. Defaults to False.

    Returns:
        tuple: If return_content is False: (bool, str) where bool is True if successful,
               False otherwise, and str is a status message.
        tuple: If return_content is True: (bool, str|None) where bool is True if successful,
               False otherwise, and str is the extracted text content or None on failure.
    """
    try:
        # --- 1. Read the HTML file ---
        # Use 'utf-8' encoding, which is common for HTML. Handle potential errors.
        with open(html_filepath, 'r', encoding='utf-8', errors='ignore') as f_html:
            html_content = f_html.read()

        # --- 2. Parse the HTML ---
        # Use BeautifulSoup. 'html.parser' is Python's built-in parser.
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- 3. Remove unwanted tags (optional but recommended) ---
        # Get rid of script and style tags, as their content is usually not desired text.
        for element in soup(["script", "style"]):
            element.decompose() # Removes the tag and its content

        # --- 4. Extract the text ---
        # soup.get_text() extracts all the text nodes.
        # 'separator="\n"' tries to put newlines between text blocks from different tags.
        # 'strip=True' removes leading/trailing whitespace from each text block.
        text_content = soup.get_text(separator='\n', strip=True)

        if return_content:
            # --- 5a. Return the content ---
            return True, text_content
        else:
            # --- 5b. Write the text to the TXT file ---
            if not txt_filepath:
                return False, "Error: txt_filepath is required when return_content is False."

            # Ensure the output directory exists
            output_dir = os.path.dirname(txt_filepath)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                except OSError as e:
                     return False, f"Error creating output directory '{output_dir}': {e}"

            # Write the extracted text using 'utf-8' encoding.
            with open(txt_filepath, 'w', encoding='utf-8') as f_txt:
                f_txt.write(text_content)

            return True, f"Successfully converted '{os.path.basename(html_filepath)}'. Output saved to: '{txt_filepath}'"

    except FileNotFoundError:
        return False, f"Error: Input HTML file not found at '{html_filepath}'" if not return_content else (False, None)
    except Exception as e:
        error_msg = f"An error occurred during conversion of '{os.path.basename(html_filepath)}': {e}"
        return False, error_msg if not return_content else (False, None)
