# Check Hashtag
Hashtag checker using a word

## Installation

```
pip install Check-Hashtag
```

## Usage

```py
import check_hashtag

print(check_hashtag.is_hashtag("#Hello"))
# => True
print(check_hashtag.is_hashtag("Hello"))
# => False 

print(check_hashtag.in_hashtag("Hello, #SupportOpensource"))
# => True
print(check_hashtag.in_hashtag("Hello, Support Opensource"))
# => False
```
