# Translations

This folder contains JSON files for **multi-language support**.  
Each JSON file represents translations for one language.

## Structure

```
translations/
├── en.json # English
├── de.json # German
├── fr.json # French
└── sr.json # Serbian
```


## JSON Format
Each JSON file should follow the same structure with nested keys:

```json
{
   "admin": {
    "dashboard": {
      "message": "Welcome {user}, you are using {platform}!"
    }
  },
  "auth": {
    "login": "Login",
    "logout": "Logout"
  },
  "users": {
    "title": "User Management",
    "create": "Create User",
    "edit": "Edit User"
  }
}
```

## Usage

Translations are loaded dynamically through the `TranslationManager` class.
You can set the active language via configuration setting `LANGUAGE` into `.env` file. 
For access to translation use `gettext` helper method which accept three parameters:
- *key* (string - separated by . for each level) - required,  
- *replacements* (dictionary) - optional
- *lang* (string) - optional

```
 {{ gettext('admin.dashboard.message', {'user': "John", 'platform': "FastKit"}) }}
```
