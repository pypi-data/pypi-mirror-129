# freetranslate

Translate your text using various APIs

## Description

This library help you to translate text from a language to other for free

## Installation

Either install from PyPI with `pip install freetranslate` or `pip install git+https://gitlab.com/tretrauit/freetranslate` to install from GitLab

## Usage

```python
import asyncio # This package uses aiohttp to do requests.
from freetranslate.googletranslate import GoogleTranslate

googletrans = GoogleTranslate()
translated_result = asyncio.run(googletrans.translate("Xin chào!", "en"))
print(translated_result.translated_text)
```

Tada, you've just translated "Xin chào!" to English and printed the translated text.

## Status

Currently this library supports Google Translate, Bing Translator & LibreTranslate

## Why another python translation library?

here's a translation library I love (py-googletrans) but its' stable branch is broken. Although there is a working one (Animenosekai/translate) but its license is AGPL 3 which is a strict license, and I don't like that. So this library was made.

## Documentation (WIP)

### class translatorabc.TranslatorABC()

Abstract class for Translators.

#### method translate(self, text: str, target_language: str, source_language: str = "auto") -> TranslateResult

Translate `text` from `source_language` (optional) to `target_language`.

#### method _parse_result(self, result: dict) -> TranslateResult

Default parser for translated result return from the server, and return a TranslateResult object.

#### method detect(self, text: str) -> str

Detect the language of `text`.

### class googletranslate.GoogleTranslate(endpoint_url: str = None, endpoint_list: list() = None) -> GoogleTranslate

This class provides Google Translate used in Google Translate extensions & clients.

### class googlewebtranslate.GoogleWebTranslate(endpoint_url: str = None, endpoint_list: list() = None) -> GoogleWebTranslate

This class provides Google Translate used in [Google Translate website](https://translate.google.com)

### class bingtranslator.BingTranslator() -> BingTranslator

This class provides Google Translate used in [Google Translate website](https://translate.google.com)

### class libretranslate.LibreTranslate(endpoint_url: str = "https://translate.argosopentech.com/") -> LibreTranslate

This class provides [LibreTranslate](https://libretranslate.com/) using their API

## Badges

On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

py-googletrans library for most code in communicating with Google RPC Translate and deobfuscation code.

## License

MIT Licensed

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
