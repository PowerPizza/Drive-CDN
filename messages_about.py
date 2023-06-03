introduction_software = """
This software help us to create our own free CDN (Content Delivery Network) using google drive's service account.
Sometimes we need such service like when we want to import our javascript, css or image files from online source
to our html file so we can use this software generally CDN services are paid and if you try to use any cloud
service as CDN to import css and javascript files so you will probably get Cross-Origin Read Blocking(CORB) error due
to cloud services don't want to use there services as CDN.
"""

how_to_use_s1 = """1. Create a new project on"""
how_to_use_s2 = """2. Select that project.
3. Click on left menu and go at [ API and services >  Enabled APIs and services ] and click on top enable API option.
4. Search for Google Drive API and select that.
5. Click on enable API.
6. Once API enabled click on menu again and go at [ IAM and admin > service accounts] and click on to CREATE SERVICE ACCOUNT option.
7. While creating service account in second stage choose both IAM roles (Security Admin, Security Reviewer) given in list.
8. Leave other optional entries.
9. click on done.
10. Now in the table of service accounts click on email field's link.
11. Select KEYS from upper options
12. Click on add keys.
13. Select create new key.
14. Select json type and click on create.
15. Now you got a json file downloaded in your computer.
16. Now come back to Drive CDN software and click on attach credentials file.
17. Choose the json file you have downloaded.
18. Ok now software is ready to use.
"""