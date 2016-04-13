import datetime
import json
import os
import pywikibot
import random
import re
import time
import types
import urllib.parse
import urllib.request


def addsection(title, summary, text):
    page = pywikibot.Page(site, title)
    result = pywikibot.site.APISite.editpage(
        site,
        page=page,
        summary=summary,
        minor=False,
        text=text,
        section="new"
    )
    return result


def allimages(start="!", prefix="", reverse=False, step=None, total=None, content=False):
    pages = pywikibot.site.APISite.allimages(
        site,
        start=start,
        prefix=prefix,
        reverse=reverse,
        step=step,
        total=total,
        content=content
    )
    return pages


def allpages(start="!", prefix="", namespace=0, filterredir=None, step=None, total=None, content=False):
    if (type(namespace) == "str"):
        namespace = site.namespaces._namespace_names["category"].id

    pages = pywikibot.site.APISite.allpages(
        site,
        start=start,
        prefix=prefix,
        namespace=namespace,
        filterredir=filterredir,
        step=step,
        total=total,
        content=content
    )

    return pages


def allredirects(start="!", prefix="", namespace=0, step=None, total=None, content=False):
    return allpages(
        start=start,
        prefix=prefix,
        namespace=namespace,
        filterredir=True,
        step=step,
        total=total,
        content=content
    )


def categorymembers(category):
    category = pywikibot.Category(site, category)
    pages = pywikibot.site.APISite.categorymembers(
        site,
        category=category
    )
    return pages


def editpage(title, summary, text, minor=True):
    page = pywikibot.Page(site, title)
    page.text = text
    result = pywikibot.site.APISite.editpage(
        site,
        page=page,
        summary=summary,
        minor=minor
    )
    return result


def embeddedin(title, filterRedirects=None, namespaces=None, step=None, total=None, content=False):
    page = pywikibot.Page(site, title)
    pages = pywikibot.site.APISite.page_embeddedin(
        site,
        page=page,
        filterRedirects=filterRedirects,
        namespaces=namespaces,
        step=step,
        total=total,
        content=content
    )
    return pages


def extlinks(title):
    page = pywikibot.Page(site, title)
    links = pywikibot.site.APISite.page_extlinks(
        site,
        page=page
    )
    return links


def logevents(title):
    page = pywikibot.Page(site, title)
    links = pywikibot.site.APISite.page_extlinks(
        site,
        page=page
    )
    return links


def movepage(title, newtitle, summary, noredirect=False):
    page = pywikibot.Page(site, title)
    page = pywikibot.site.APISite.movepage(
        site,
        page=page,
        newtitle=newtitle,
        summary=summary,
        noredirect=noredirect
    )
    return page


def newfiles(user=None, start=None, end=None, reverse=False, step=None, total=None):
    files = pywikibot.site.APISite.newfiles(
        site,
        start=start,
        end=end,
        reverse=reverse,
        step=step,
        total=total
    )
    return files


def pagebacklinks(title, followRedirects=False, filterRedirects=None, namespaces=None, step=None, total=None, content=False):
    page = pywikibot.Page(site, title)
    pages = pywikibot.site.APISite.pagebacklinks(
        site,
        page=page,
        followRedirects=followRedirects,
        filterRedirects=filterRedirects,
        namespaces=namespaces,
        step=step,
        total=total,
        content=content
    )
    return pages


def pagelinks(title):
    page = pywikibot.Page(site, title)
    pages = pywikibot.site.APISite.pagelinks(
        site,
        page=page
    )
    return pages


def get_abuselog():
    url = "https://en.wikiversity.org/w/api.php?action=query&list=abuselog&format=json&aflprop=details"
    page = urllib.request.urlopen(url).read()
    print(page)


def get_allpages(prefix="", namespace=0, filterredir=None, content=False):
    result = []
    start = "!"
    while (True):
        pages = allpages(start=start, prefix=prefix, namespace=namespace, filterredir=filterredir, content=content)
        if (pages == None):
            break
        start = pages[-1].title() + "!"


def get_namespaces():
    namespaces = site.namespaces()
    for namespace in namespaces:
        print(namespace)


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))


def files_missing_license(start, end):
    tags = [
        "{{information",
        "{{pd",
        "{{cc-by",
        "{{gfdl",
        "{{self",
        "{{bsd",
        "{{gpl",
        "{{lgpl",
        "{{free",
        "{{copyright",
        "{{fairuse",
        "{{non-free",
        "{{software",
        "{{no license",
        "{{no fairuse",
        "{{wikiversity-screenshot"
    ]

    files = newfiles(
        start=start,
        end=end,
        reverse=True)

    result = list()

    for file in files:
        if not file[0].exists():
            continue
        text = file[0].text.lower()
        if not (any(word in text for word in tags)):
            result.append(file)

    return result


def filekey(file):
    return file[2] + file[0].title()


def add_missing_license_information(days):
    start = (datetime.datetime.now() + datetime.timedelta(-days)).strftime("%Y-%m-%d 00:00:00")
    end = (datetime.datetime.now() + datetime.timedelta(1)).strftime("%Y-%m-%d 00:00:00")
    usermsg = (
        "Thank you for uploading files to Wikiversity. See [[Wikiversity:Media]] for copyright and license requirements "
        "for Wikiversity files. All files must have copyright and/or license information added to the file.\n\n"
        "Instructions for adding copyright and/or license information are available at [[Wikiversity:License tags]]. "
        "Files must be updated within seven days or they may be removed without further notice.\n\n"
        "The following files are missing copyright and/or license information:\n"
    )
    summary = "Missing License Information"

    files = files_missing_license(start, end)
    files = sorted(files, key=filekey)
    user = ""
    print("== Files Missing License Information ==")
    for file in files:
        if user != file[2]:
            if user != "":
                title = "User_talk:" + user
                text += "\n~~~~\n"
                addsection(title, summary, text)
            user = file[2]
            text = usermsg
            print(";[[User_talk:" + user + "]]")
        title = file[0].title()
        text += "* [[:" + title + "]]\n"
        print(":[[:" + title + "]]")
        addsection(title, summary, "{{subst:nld}}")
    if user != "":
        title = "User_talk:" + user
        text += "\n~~~~\n"
        addsection(title, summary, text)


def show_sister_backlinks(wiki, language="en"):
    global site

    site = pywikibot.Site(language, wiki.lower())
    pages = embeddedin(title="Template:Wikiversity", namespaces=0, content=True)
    pages = sorted(pages)
    for page in pages:
        title = page.title()
        regex = re.compile("{{wikiversity[^}]*}}", re.IGNORECASE)
        match = regex.search(page.text)
        if (match == None):
            continue

        text = match.group()
        if (text.lower() == "{{wikiversity}}"):
            print("* [[" + wiki + ":" + title + "]] -> [[" + title + "]]")
            continue

        match = re.search("\|[^|}]*[|}]", text)
        if (match != None):
            text = match.group()
            text.replace("at=", "")
            print("* [[" + wiki + ":" + title + "]] -> [[" + text[1:-1] + "]]")
            continue

        print(title + " -> " + text)


def find_pages():
    pages = allpages(content=False)
    for page in pages:
        title = page.title()
        if (title.find("\\") >= 0):
            print("* [[" + page.title() + "]]")
            # movepage(title, newtitle, "Renaming")


def get_empty_categories():
    categories = allcategories()
    for category in categories:
        title = category.title()
        members = categorymembers(title[9:])
        count = 0
        for member in members:
            count += 1
            break
        if (count == 0):
            print("* [[:" + title + "]]")


def get_schools():
    categories = allcategories()
    for category in categories:
        title = category.title()
        members = categorymembers(title[9:])
        count = 0
        for member in members:
            count += 1
            break
        if (count == 0):
            print("* [[:" + title + "]]")


def fix_box_transclude():
    pages = allpages(namespace="Portal", content=True)
    regex = re.compile("{{\/box-header.*\n.*\n{{\/box-footer\|}}", re.IGNORECASE)
    for page in pages:
        title = page.title()
        text = page.text
        result = ""
        save = False
        if(text.find("box-header") >= 0):
            print(title)
            while(True):
                match = regex.search(text, )
                if(match == None):
                    break
                lines = match.group(0).split("\n")
                list = lines[0].split("|")
                textlink = list[2]
                if(lines[1].find(textlink) < 0):
                    result = result + text[0:match.end(0)]
                    text = text[match.end(0):]
                    continue
                texttitle = list[1]
                texttitle = texttitle.replace("''", "")
                if(textlink.find("{{FULLPAGENAME}}/") == 0):
                    textlink = textlink[17:]
                if(textlink == texttitle):
                    replace = "{{box-transclude|" + textlink + "}}"
                else:
                    replace = "{{box-transclude|" + textlink + "|" + texttitle + "}}"
                save = True
                result = result + text[0:match.start(0)] + replace
                text = text[match.end(0):]
            result = result + text
            page.text = result
            if(save):
                page.save(summary="Box-transclude", minor=True, botflag=True)
            #print(result)

def clean_photoshop():
    pages = allpages(prefix="Adobe Photoshop", content=True)
    regex = re.compile("''\[\[Topic:Photoshop\| ↑ Back to Photoshop\]\]''\n", re.IGNORECASE)
    for page in pages:
        text = page.text
        match = regex.search(text)
        if match == None:
            continue
        print(page.title())
        text = text[0:match.start(0)] + text[match.end(0):]
        while(text[0:1] == "\n"):
            text = text[1:]
        page.text = text
        page.save(summary="Removing unnecessary backlinks.", minor=True, botflag=True)


def change_category(source, destination):
    category = pywikibot.Category(site, source)
    pages = site.categorymembers(category, content=True)
    regex = re.compile("\[\[Category: *" + source + "[^\]]*\]\]\n?", re.IGNORECASE)
    for page in pages:
        title = page.title()
        print(page.title())
        text = page.text
        match = regex.search(text)
        if match == None:
            continue
        if destination == "":
            text = text[0:match.start(0)] + text[match.end(0):]
            summary = "Removing category [[:Category:" + source + "]]"
        else:
            text = text[0:match.start(0)] + "[[Category:" + destination + "]]\n" + text[match.end(0):]
            summary = "Changing category from [[:Category:" + source + "]] to [[:Category:" + destination + "]]"
        page.text = text
        page.save(summary=summary, minor=True, botflag=True)


def remove_category(page, category):
    regex = re.compile("\[\[Category: *" + category + "[^\]]*\]\]\n?", re.IGNORECASE)
    text = page.text
    match = regex.search(text)
    if match != None:
        text = text[0:match.start(0)] + text[match.end(0):]
        page.text = text
        summary = "Removing Category:" + category + "."
        page.save(summary=summary, minor=True, botflag=True)


def fix_box_transclude_apostrophes():
    pages = embeddedin("Template:Box-transclude", content=True)
    regex = re.compile("{{box-transclude.*'.*'}}", re.IGNORECASE)
    for page in pages:
        text = page.text
        match = regex.search(text)
        if match == None:
            continue

        print(page.title())
        save = False
        while(True):
            match = regex.search(text)
            if(match == None):
                break
            replace = match.group(0).replace("'", "")
            list = replace.split("|")
            list[2] = list[2].replace("}}", "")
            if(list[1] == list[2]):
                replace = replace.replace("|" + list[1], "", 1)
            text = text[0:match.start(0)] + replace + text[match.end(0):]
            save = True

        page.text = text
        if(save):
            page.save(summary="Box-transclude Cleanup", minor=True, botflag=True)


def fix_portal_box_header():
    pages = embeddedin("Portal:Box-header", content=True)
    for page in pages:
        text = page.text
        regex = re.compile("{{portal:box-header", re.IGNORECASE)
        match = regex.search(text)
        if match == None:
            continue

        print(page.title())
        continue

        save = False

        regex = re.compile("{{Portal:Box-header", re.IGNORECASE)
        match = regex.search(text)
        if(match != None):
            text = text[0:match.start(0)] + "{{Box-header" + text[match.end(0):]
            save = True

        while(True):
            match = re.search("\s\|", text)
            if match == None:
                break
            if(text[match.start(0)] != "\n"):
                text = text[0:match.start(0)] + "\n|" + text[match.end(0):]
                save = True
            break

        while(True):
            match = re.search("\|\s", text)
            if match == None:
                break
            text = text[0:match.start(0)] + "|" + text[match.end(0):]
            save = True

        while(True):
            match = re.search("<!--.*-->", text)
            if match == None:
                break
            text = text[0:match.start(0)] + text[match.end(0):]
            save = True

        while(True):
            match = re.search("\s\n", text)
            if match == None:
                break
            text = text[0:match.start(0)] + "\n" + text[match.end(0):]
            save = True

        while(True):
            match = re.search("\s$", text)
            if match == None:
                break
            text = text[0:match.start(0)]
            save = True

        if text[-3] != "\n":
            text = text[0:-2] + "\n" + text[-2:]
            save = True

        if(save):
            page.text = text
            page.save(summary="[[Portal:Box-header]] -> [[Template:Box-header]]", minor=True, botflag=True)


def fix_portal_box_footer():
    pages = embeddedin("Portal:Box-footer", content=True)
    regex = re.compile("\{\{portal:box-footer.*\}\}", re.IGNORECASE | re.DOTALL)
    for page in pages:
        text = page.text
        match = regex.search(text)
        if match == None:
            continue

        if(page.title().find("/box-footer") < 0):
            continue

        print(page.title())
        text = text[0:match.start(0)] + "{{Box-footer" + text[match.start(0) + 19:]

        page.text = text
        page.save(summary="[[Portal:Box-footer]] -> [[Template:Box-footer]]", minor=True, botflag=True)


def fix_review_questions():
    pages = allpages(prefix="Project Management/", content=True)
    regex = re.compile("\{\{collapsible toggle", re.IGNORECASE)
    for page in pages:
        title = page.title()

        if title.find("flashcards") >= 0:
            continue

        text = page.text
        match = regex.search(text)
        if(match == None):
            continue

        print(page.title())

        while(True):
            match = regex.search(text)
            if(match == None):
                break
            start = match.start(0)
            end = text.find("}}", start) + 2
            result = text[start:end]
            list = result.split("\n")
            list[0] = "{{review question"
            #index = list[1].find(" ")
            #list[1] = "|" + list[1][index + 1:]
            list[1] = "|" + list[1]
            result = "\n"
            result = result.join(list)
            result = result.replace("| ", "|")
            text = text[0:start] + result + text[end:]

        index = text.find("{{review question")
        text = text[0:index] + "{{review start}}\n" + text[index:]

        index = text.rfind("{{review question")
        index = text.find("}}", index) + 3
        text = text[0:index] + "{{review end}}\n" + text[index:]

        text = text.replace("\n\n{{review question", "\n{{review question")

        page.text = text
        #print(text)
        page.save(summary="[[Template:Collapsible toggle]] -> [[Template:Review question]]", minor=True, botflag=True)


def fix_double_redirect(title):
    page = pywikibot.Page(site, title)
    regex = re.compile("#REDIRECT ?\[\[[^\]]*\]\]", re.IGNORECASE)
    if (page.isRedirectPage()):
        fix = False
        target = page.getRedirectTarget()
        while (target.isRedirectPage()):
            fix = True
            target = target.getRedirectTarget()

        if (fix == False):
            return

        text = page.text
        match = regex.search(text)
        if match == None:
            return

        print(page.title())
        text = text[0:match.start(0)] + "#REDIRECT [[" + target.title() + "]]" + text[match.end(0):]
        page.text = text
        summary = "Fixing double redirect from [[" + page.getRedirectTarget().title() + "]] to [[" + target.title() + "]]"
        page.save(summary=summary, minor=True, botflag=True)


def fix_double_redirects():
    url = "https://en.wikiversity.org/w/index.php?title=Special:DoubleRedirects&limit=500&offset=0"
    text = urllib.request.urlopen(url).read()
    text = text.decode("UTF-8")
    lines = re.findall("<li>(.+?)<\/li>", text)
    for line in lines:
        if line.find("<del>") >= 0:
            continue
        titles = re.findall('<a.+?>(.+?)<\/a>', line)
        for title in titles:
            if(title != "(edit)"):
                fix_double_redirect(title)


def fix_portals():
    pages = embeddedin("Template:Portals", content=True)
    regex = re.compile("{\{Portals\}\}", re.IGNORECASE)
    for page in pages:
        title = page.title()
        text = page.text
        match = regex.search(text)
        if match == None:
            continue

        if(title.find("Portal:GreySmith") >= 0):
            continue

        if(text.find("{{Portals}}\n{{/box-footer|}}") >= 0):
            continue

        print(title)
        continue

        if(text.find("box-transclude") < 0):
            print("*** No box ***")
            continue

        text = text[0:match.start(0)] + \
               "{{/box-header|Major Wikiversity Portals|{{FULLPAGENAME}}}}\n{{Portals}}\n{{/box-footer|}}" + \
               text[match.end(0):]
        page.text = text
        page.save(summary="Adding box around {{Portals}}.", minor=True, botflag=True)


def fix_category():
    pages = allpages(prefix="Primary mathematics/", content=True)

    regex = re.compile("\[\[Category:School of Mathematics\]\]\n?", re.IGNORECASE)
    for page in pages:
        #page = pywikibot.Page(site, title=page)
        text = page.text
        match = regex.search(text)
        if match == None:
            continue
        print(page.title())
        text = text[0:match.start(0)] + "{{CourseCat}}\n" + text[match.end(0):]
        page.text = text
        page.save(summary="Changing category from School of Mathematics to CourseCat.", minor=True, botflag=True)


def delete_broken_redirects():
    regex = re.compile("#REDIRECT \[\[[^\]]*\]\]", re.IGNORECASE)
    pages = site.broken_redirects()
    for page in pages:
        if not page.exists():
            continue
        text = page.text
        match = regex.search(text)
        if match == None:
            continue
        print(page.title())
        text = match.group(0)
        index = text.find("[")
        text = text[index:]
        site.deletepage(page=page, reason="Broken redirect to " + text)


def unblock_IPs():
    random.seed()
    blocks = site.blocks(reverse=True)
    list = []
    for block in blocks:
        try:
            if block['rangestart'] == '0.0.0.0':
                continue
            if block['expiry'] != 'infinity':
                continue
        except:
            continue

        ip = block['user']
        list.append(ip)

    list.sort()
    count = 0
    maxcount = len(list)
    for ip in list:
        #print("* https://en.wikiversity.org/wiki/Special:Unblock/" + ip + "?wpReason=Removing%20ancient%20indefinite%20block%20on%20IP%2E")
        #print("* https://en.wikiversity.org/w/index.php?title=User_talk:" + ip + "&action=delete")

        try:
            user = pywikibot.User(site, title=ip)
            title = user.title()
            print(title)
            site.unblockuser(user, "Removing ancient indefinite block on IP.")
            #time.sleep(10)

            title = title.replace("User:", "User_talk:")
            page = pywikibot.Page(site, title=title)
            print(page.title())
            site.deletepage(page=page, reason="Deleting openproxy block notice.")
            #time.sleep(10)
        except:
            time.sleep(60)

        count += 1
        if count % maxcount == 0:
            exit(0)
        minutes = (maxcount - count) * 2 * 10 / 60
        print("Estimated completion in " + str(minutes) + " minutes.")


def print_user_talk_pages(prefix):
    pages = allpages(prefix=prefix, namespace=3)
    for page in pages:
        title = page.title()
        if title.find(".") < 0:
            continue
        time = page.editTime()
        if str(time) > "2015":
            continue
        print("* [[" + title + "]]")


def find_Level_1_headings():
    regex = re.compile("^=[^=]*= *$", re.MULTILINE)
    pages = allpages(content=True)

    for page in pages:
        text = page.text
        match = regex.search(text)
        if match == None:
            continue
        print("* [[" + page.title() + "]]")
        continue

        if text.find("[[Category:Pages with Level 1 heading]]") >= 0:
            continue
        print(page.title())
        text = text.strip()
        text = text + "\n[[Category:Pages with Level 1 heading]]\n"
        page.text = text
        page.save(summary="Adding [[Category:Pages with Level 1 heading]].", minor=True, botflag=True)


def purge_pages():
    pages = embeddedin("Module:Yesno")
    found = False
    for page in pages:
        title = page.title()
        if title == "Template:L/doc":
            found = True
        if not found:
            continue

        print(title)
        url = page.full_url()
        url = url + "?action=purge"
        urllib.request.urlopen(url).read()


def fix_Level1_headings(title):
    print(title)

    page = pywikibot.Page(site, title)
    text = page.text
    if text.find("======") >= 0:
        print("Unexpected heading level")
        exit(0)

    regex = re.compile("^=[^=]*= *$", re.MULTILINE)
    match = regex.search(text)
    if match != None:

        regex = re.compile("^==[^=]*== *$", re.MULTILINE)
        match = regex.search(text)
        if match != None:
            regex = re.compile("^=====[^=]*===== *$", re.MULTILINE)
            while(True):
                match = regex.search(text)
                if match == None:
                    break
                text = text[0:match.start(0)] + "=" + text[match.start(0):match.end(0)].strip() + "=" + text[match.end(0):]

            regex = re.compile("^====[^=]*==== *$", re.MULTILINE)
            while(True):
                match = regex.search(text)
                if match == None:
                    break
                text = text[0:match.start(0)] + "=" + text[match.start(0):match.end(0)].strip() + "=" + text[match.end(0):]

            regex = re.compile("^===[^=]*=== *$", re.MULTILINE)
            while(True):
                match = regex.search(text)
                if match == None:
                    break
                text = text[0:match.start(0)] + "=" + text[match.start(0):match.end(0)].strip() + "=" + text[match.end(0):]

            regex = re.compile("^==[^=]*== *$", re.MULTILINE)
            while(True):
                match = regex.search(text)
                if match == None:
                    break
                text = text[0:match.start(0)] + "=" + text[match.start(0):match.end(0)].strip() + "=" + text[match.end(0):]

        regex = re.compile("^=[^=]*= *$", re.MULTILINE)
        while(True):
            match = regex.search(text)
            if match == None:
                break
            text = text[0:match.start(0)] + "=" + text[match.start(0):match.end(0)].strip() + "=" + text[match.end(0):]

    text = text.replace("[[Category:Pages with Level 1 heading]]", "")

    if page.text != text:
        page.text = text
        page.save(summary="Replacing Level 1 headings with Level 2 headings.", minor=True, botflag=True)


def fix_file_information():
    user = pywikibot.User(site, "Franz Kies")
    contributions = user.contributions()
    for contribution in contributions:
        page = contribution[0]
        title = page.title()
        if title.find("File:") < 0:
            continue

        text = page.text
        if text.find("{{information") >= 0:
            continue
        if text.find("{{Information") >= 0:
            continue

        if text.find("self") < 0:
            continue

        print(title)

        #match = re.search("\|.*Description\n\|(.*)\n", text)
        #if match == None:
        #    print("No description")
        #    continue
        #description = match.group(1).strip()

        match = re.search("== Summary ==\n(.*)\n", text)
        if match == None:
            print("No description")
            continue
        description = match.group(1).strip()

        #match = re.search("\|.*Source\n\|(.*)\n", text)
        #if match == None:
        #    print("No source")
        #    continue
        #source = match.group(1).strip()
        source = "Self"

        filepage = pywikibot.FilePage(site, title)
        date = filepage.latest_file_info.timestamp.strftime("%d %B %Y")

        #match = re.search("\|.*Author\n\|(.*)\n", text)
        #if match == None:
        #    print("No author")
        #    continue
        #author = match.group(1).strip()
        author = "Franz Kies"

        #match = re.search("\|.*Permission\n\|(.*)\n", text)
        #if match == None:
        #    print("No permission")
        #    continue
        #permission = match.group(1).strip()
        permission = "GDFL"

        match = re.search("== Licensing ==\n(.*)", text)
        if match == None:
            print("No licensing")
            continue
        license = match.group(1).strip()

        information = "{{Information\n"
        information += "|Description=" + description + "\n"
        information += "|Source=" + source + "\n"
        information += "|Date=" + date + "\n"
        information += "|Author=" + author + "\n"
        information += "|Permission=" + permission + "\n"
        information += "}}\n\n"

        text = "== Summary ==\n" + information + "== Licensing ==\n" + license
        page.text = text
        page.save(summary="Replacing table-based information with [[Template:Information]].", minor=True, botflag=True)

def get_pageviews(wiki, title, start, end):
    title = title.replace(" ", "_")
    title = urllib.parse.quote(title)
    title = title.replace("/", "%2f")
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"\
        + wiki + "/all-access/user/"\
        + title + "/daily/" + start + "/" + end
    try:
        page = urllib.request.urlopen(url).read()
    except:
        print("Error reading " + url)
        return -1

    page = page.decode("UTF-8")

    items = json.loads(page)
    views = 0
    for item in items["items"]:
        views += int(item["views"])

    start = datetime.datetime.strptime(start, "%Y%m%d")
    end = datetime.datetime.strptime(end, "%Y%m%d")
    days = (end - start).days
    if days > 0:
        return views / days
    else:
        return None


def tag_unused_fairuse_files():
    pages = categorymembers("Fair use images")
    for page in pages:
        title = page.title()

        if title.find("File:") != 0:
            continue

        links = site.imageusage(page)

        count = 0
        for link in links:
            count += 1
            break

        if count != 0:
            continue

        print(title)

        text = page.text

        text = "{{Delete|Unused [[Wikiversity:Fair use|fair use]] file.}}\n\n" + text

        if page.text != text:
            page.text = text
            page.save("Unused [[Wikiversity:Fair use|fair use]] file.", minor=False, botflag=True)


def fix_from_page_history():
    #page = pywikibot.Page(site, "File:Eml5526 s11 team2 hw2 4 6.jpg")
    #text = page.text
    #start = text.find("== Licensing ==\n") + 16
    #end = text.find("|}") + 2
    #license = text[start:end]
    #license = "{{CC-by-sa-3.0-dual}}"

    for title in titles:
        page = pywikibot.Page(site, title)
        history = page.fullVersionHistory()

        if history[0].timestamp.strftime("%Y%m%d") >= "20160319":
            continue

        print(title)
        text = history[1].text

        text = text.replace("\n\n", "\n")

        if text.find("{{CC-by-sa-3.0-dual}}") < 0:

            if text.lower().find("multi-licensed") < 0 and text.find("MultiLicense") < 0:
                print("Not multi-licensed: " + title)
                exit(0)

            if text[0] == "(":
                text = text[1:]

            if text [-1] == ")":
                text = text[0:-2]

            index = text.find("|")
            if text[index - 1] != "\n":
                index = 0
                while True:
                    index = text.find("|", index + 1)
                    if index < 0:
                        break
                    if text[index - 1] != "\n":
                        text = text[0:index - 1] + "\n" + text[index:]
                        index += 1

            index = text.find("}}")
            if text[index - 1] != "\n":
                text = text[0:index - 1] + "\n" + text[index:]

            index = text.find("== Licensing ==")
            if index > 0 and text[index - 1] != "\n":
                text = text[0:index - 1] + "\n\n" + text[index:]

            index = text.find("== Licensing ==")
            if index > 0 and text[index + 15] != "\n":
                text = text[0:index + 15] + "\n" + text[index + 17:]

            index = text.find("|}", index)
            if index > 0 and text[index + 2] != "\n":
                text = text[0:index + 2] + "\n\n" + text[index + 3:]

            start = text.find("== Licensing ==\n") + 16
            if start < 16:
                text = text + "\n\n== Licensing ==\n"
                start = len(text)

            end = text.find("|}", start) + 2
            if end < 2:
                end = text.lower().find("\n[[category")
                if end < 0:
                    end = len(text)

            text = text[0:start] + "{{CC-by-sa-3.0-dual}}" + text[end:]

            if text.find("}}\n== Licensing ==") >= 0:
                text = text.replace("}}\n== Licensing ==", "}}\n\n== Licensing ==")

        if text.find("{{CC-by-sa-3.0-dual}}\n[[") >= 0:
            text = text.replace("{{CC-by-sa-3.0-dual}}\n[[", "{{CC-by-sa-3.0-dual}}\n\n[[")

        text = text.replace("<br>", "")

        print(text)
        #exit(0)

        page.text = text
        page.save("Correcting [[Template:CC-by-sa-3.0-dual]].", minor=True, botflag=True)


def generate_topic_review():
    result = "Pages in the Topic namespace as of " + time.strftime("%Y %B %d") + " for review. "
    result += "Last Edit, Total Edits and Total Editors do not include bots. "
    result += "Daily Views is the average daily views from 2015-10-01 to 2016-02-29. "
    result += "Links are incoming links, not counting this page.\n"
    result += "\n"
    result += '{| class="wikitable sortable"\n'
    result += "|-\n"
    result += "! Page !! Created !! Last Edit !! Total Edits !! Total Editors !! Length !! Subpages !! Links !! Daily Views !! Status"
    print(result)
    result += "\n"

    pages = pywikibot.site.APISite.allpages(site, namespace=104)
    for page in pages:
        title = page.title()
        if title.find("/") >= 0:
            continue
        text = page.text

        history = page.getVersionHistory()
        created = history[-1].timestamp.date()

        users = dict()
        lastedit = None
        for entry in history:
            user = entry.user.title()
            if user.lower().find("bot") >= 0:
                continue
            if lastedit == None:
                lastedit = entry.timestamp.date()
            if user in users:
                users[user] += 1
            else:
                users[user] = 1

        edits = 0
        for user in users:
            edits += users[user]

        editors = len(users)
        length = len(text)

        subpages = pywikibot.site.APISite.allpages(site, prefix=title.replace("[[Topic:", "").replace("]]", "/"), namespace=104, filterredir=False)
        subpage_count = 0
        for subpage in subpages:
            subpage_count += 1

        links = page.backlinks()
        link_count = 0
        for link in links:
            if link.title() == "Wikiversity:Topic Review":
                continue
            link_count += 1

        views = get_pageviews("en.wikiversity", title, "20151001", "20160229")

        if page.isRedirectPage():
            status = "redirect"
        elif text.lower().find("{{proposed deletion") >= 0:
            status = "proposed deletion"
        elif text.lower().find("{{merge") >= 0:
            status = "merge"
        else:
            status = ""

        line = "|-\n|" + "[[" + title + "]]"
        line += "||" + str(created).replace("-", "&#8209;")
        line += "||" + str(lastedit).replace("-", "&#8209;")
        line += "||" + str(edits)
        line += "||" + str(editors)
        line += "||" + str(length)
        line += "||" + str(subpage_count)
        line += "||" + str(link_count)
        line += "||" + '{0:.2f}'.format(views)
        line += "||" + str(status).replace(" ", "&nbsp;")
        print(line)
        result += line + "\n"

    result += "|}\n\n[[Category:Wikiversity]]\n"
    page = pywikibot.Page(site, "Wikiversity:Topic Review")
    page.text = result
    page.save(summary="Update", minor=True, botflag=True)


def update_topic_review():
    page = pywikibot.Page(site, "Wikiversity:Topic Review")
    text = page.text
    lines = text.split("\n")
    result = "Pages in the Topic namespace as of " + time.strftime("%Y %B %d") + " for review. "
    result += "Last Edit, Total Edits and Total Editors do not include bots. "
    result += "Daily Views is the average daily views from 2015-10-01 to 2016-02-29. "
    result += "Links are incoming links, not counting this page.\n"
    result += "\n"
    result += '{| class="wikitable sortable"\n'
    result += "|-\n"
    result += "! Page !! Created !! Last Edit !! Total Edits !! Total Editors !! Length !! Subpages !! Links !! Daily Views !! Status"
    print(result)
    result += "\n"
    for line in lines:
        if line[0:9] != "|[[Topic:":
            continue

        match = re.search("\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)", line)
        title = match.group(1).replace("[[", "").replace("]]", "")
        created = match.group(2).replace("&#8209;", "-")
        lastedit = match.group(3).replace("&#8209;", "-")
        edits = int(match.group(4))
        editors = int(match.group(5))
        length = int(match.group(6))
        subpage_count = int(match.group(7))
        link_count = int(match.group(8))
        views = match.group(9)
        status = match.group(10).replace("&nbsp;", " ")

        # page = pywikibot.Page(site, title)
        # if page == None:
        #     continue
        # if not page.exists():
        #     continue

        # text = page.text
        # if len(text) == 0:
        #     continue

        # history = page.getVersionHistory()
        # created = history[-1].timestamp.date()
        #
        # users = dict()
        # lastedit = None
        # for entry in history:
        #     user = entry.user.title()
        #     if user.lower().find("bot") >= 0:
        #         continue
        #     if lastedit == None:
        #         lastedit = entry.timestamp.date()
        #     if user in users:
        #         users[user] += 1
        #     else:
        #         users[user] = 1
        #
        # edits = 0
        # for user in users:
        #     edits += users[user]
        #
        # editors = len(users)
        # length = len(text)

        subpages = pywikibot.site.APISite.allpages(site, prefix=title.replace("Topic:", "") + "/", namespace=104, filterredir=False)
        subpage_count = 0
        for subpage in subpages:
            subpage_count += 1

        # links = page.backlinks()
        # link_count = 0
        # for link in links:
        #     if link.title() == "Wikiversity:Topic Review":
        #         continue
        #     link_count += 1

        # if views == "":
        #     views = get_pageviews("en.wikiversity", title, "20151001", "20160229")
        #     if views == -1:
        #         views = ""
        #     else:
        #         views = '{0:.2f}'.format(views)

        # if page.isRedirectPage():
        #      status = "redirect"
        # elif text.lower().find("{{proposed deletion") >= 0:
        #     status = "proposed deletion"
        # elif text.lower().find("{{merge") >= 0:
        #     status = "merge"
        # else:
        #     status = ""

        line = "|-\n|" + "[[" + title + "]]"
        line += "||" + str(created).replace("-", "&#8209;")
        line += "||" + str(lastedit).replace("-", "&#8209;")
        line += "||" + str(edits)
        line += "||" + str(editors)
        line += "||" + str(length)
        line += "||" + str(subpage_count)
        line += "||" + str(link_count)
        line += "||" + views
        line += "||" + str(status).replace(" ", "&nbsp;")
        print(line)
        result += line + "\n"

    result += "|}\n\n[[Category:Wikiversity]]\n"
    page = pywikibot.Page(site, "Wikiversity:Topic Review")
    page.text = result
    page.save(summary="Update", minor=True, botflag=True)


def delete_unused_topic_redirects():
    page = pywikibot.Page(site, "Wikiversity:Topic Review")
    text = page.text
    lines = text.split("\n")

    for line in lines:
        if line[0:9] != "|[[Topic:":
            continue

        match = re.search("\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)", line)
        title = match.group(1).replace("[[", "").replace("]]", "")
        created = match.group(2).replace("&#8209;", "-")
        lastedit = match.group(3).replace("&#8209;", "-")
        edits = int(match.group(4))
        editors = int(match.group(5))
        length = int(match.group(6))
        subpage_count = int(match.group(7))
        views = match.group(8)
        status = match.group(9).replace("&nbsp;", " ")

        if views == "":
            views = -1
        else:
            views = float(views)

        if created >= "2016-01-01":
            continue

        if lastedit >= "2016-01-01":
            continue

        if subpage_count > 0:
            continue

        if status != "redirect":
            continue

        if views >= 0.5:
            continue

        page = pywikibot.Page(site, title)
        if page == None:
            continue
        if not page.exists():
            continue
        if not page.isRedirectPage():
            continue

        text = page.text
        if len(text) == 0:
            continue

        links = page.backlinks()

        link_count = 0
        for link in links:
            if link.title() == "Wikiversity:Topic Review":
                continue
            if link.title() == "Topic:Topics":
                continue
            link_count += 1
            break

        if link_count > 0:
            continue

        print(title)

        regex = re.compile("#REDIRECT ?(\[\[.*?\]\])", re.IGNORECASE)
        text = page.text
        match = regex.search(text)
        if match == None:
            print("Not found")
            continue

        reason = "Unused redirect to " + match.group(1)
        page.delete(reason, prompt=False)


def fix_page_links(title):
    page = pywikibot.Page(site, title)
    text = page.text

    list = []
    for match in re.finditer("\[\[([^\|\]]*)\|?.*?\]\]", text):
        link = pywikibot.Page(site, match.group(1).strip())
        if link == None:
            continue
        if link.isRedirectPage():
            while link.isRedirectPage():
                link = link.getRedirectTarget()
            item = match.start(1), link.title(), match.end(1)
            list.append(item)

    for item in reversed(list):
        text = text[0:item[0]] + item[1] + text[item[2]:]

    if page.text != text:
        page.text = text
        summary = "Fixing links to moved pages."
        page.save(summary=summary, minor=True, botflag=True)


def generate_category_review():
    result = "Pages in the Category namespace as of " + time.strftime("%Y %B %d") + " for review. "
    result += "Daily Views is the average daily views from 2015-10-01 to 2016-02-29. "
    result += "\n"
    result += '{| class="wikitable sortable"\n'
    result += "|-\n"
    result += "! Category !! Subcategories !! Pages !! Files !! Daily Views"
    print(result)
    result += "\n"

    categories = site.allpages(namespace=14)
    for category in categories:
        title = category.title()

        members = site.categorymembers(category=category, member_type="subcat")
        subcategory_count = 0
        for member in members:
            subcategory_count += 1

        members = site.categorymembers(category=category, member_type="page")
        page_count = 0
        for member in members:
            page_count += 1

        members = site.categorymembers(category=category, member_type="file")
        file_count = 0
        for member in members:
            file_count += 1

        views = get_pageviews("en.wikiversity", title, "20151001", "20160229")
        if views == -1:
            views = ""
        else:
            views = '{0:.2f}'.format(views)

        line = "|-\n|" + "[[:" + title + "]]"
        line += "||" + str(subcategory_count)
        line += "||" + str(page_count)
        line += "||" + str(file_count)
        line += "||" + views
        print(line)
        result += line + "\n"

    result += "|}\n\n[[Category:Wikiversity]]\n"
    page = pywikibot.Page(site, "Wikiversity:Category Review")
    page.text = result
    page.save(summary="Update", minor=True, botflag=True)


def update_category_review():
    page = pywikibot.Page(site, "Wikiversity:Category Review")
    text = page.text
    lines = text.split("\n")
    result = "Pages in the Category namespace as of " + time.strftime("%Y %B %d") + " for review. "
    result += "Daily Views is the average daily views from 2015-10-01 to 2016-02-29. "
    result += "Links are incoming links, not counting this page.\n"
    result += "\n"
    result += '{| class="wikitable sortable"\n'
    result += "|-\n"
    result += "! Category !! Subcategories !! Pages !! Files !! Links !! Daily Views"
    print(result)
    result += "\n"

    for line in lines:
        if line[0:13] != "|[[:Category:":
            continue

        match = re.search("\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)\|\|(.*)", line)
        title = match.group(1).replace("[[:", "").replace("]]", "")
        subcategory_count = int(match.group(2))
        page_count = int(match.group(3))
        file_count = int(match.group(4))
        link_count = int(match.group[5])
        views = match.group(6)

        if title <= "Category:User:renepick/test":
            continue

        page = pywikibot.Page(site, title)

        # links = page.backlinks()
        # link_count = 0
        # for link in links:
        #     if link.title() == "Wikiversity:Category Review":
        #         continue
        #     link_count += 1

        if views == "":
            views = get_pageviews("en.wikiversity", title, "20151001", "20160229")
            if views == -1:
                views = ""
            else:
                views = '{0:.2f}'.format(views)

        line = "|-\n|" + "[[:" + title + "]]"
        line += "||" + str(subcategory_count)
        line += "||" + str(page_count)
        line += "||" + str(file_count)
        line += "||" + str(link_count)
        line += "||" + views
        print(line)
        result += line + "\n"

    result += "|}\n\n[[Category:Wikiversity]]\n"
    page = pywikibot.Page(site, "Wikiversity:Category Review")
    page.text = result
    page.save(summary="Update", minor=True, botflag=True)


def user_contributions(user):
    contributions = site.usercontribs(user)

    titles = []
    for contribution in contributions:
        title = contribution['title']
        if title not in titles:
            titles.append(title)

    titles = sorted(titles)

    pages = []
    for title in titles:
        page = pywikibot.Page(site, title)
        pages.append(page)

    return(pages)


def user_files(user):
    contributions = site.usercontribs(user)

    titles = []
    for contribution in contributions:
        title = contribution['title']
        if title.find("File:") != 0:
            continue
        if title not in titles:
            titles.append(title)

    titles = sorted(titles)

    pages = []
    for title in titles:
        page = pywikibot.FilePage(site, title)
        pages.append(page)

    return(pages)


def fix_Use_TeX():
    text = ""
    start = text.find("{{Use TeX")
    end = text.find("}}", start)
    description = text[0:start] + text[end + 2:]
    description = description.replace("\n", "").strip()
    if description == "":
        description = "{{PAGENAME}}"
    license = text[start:end + 2]

    upload = page.getLatestUploader()
    user = "[[User:" + upload[0] + "]]"
    date = upload[1]

    text = "== Summary ==\n"
    text += "{{Information\n"
    text += "|Description=" + description + "\n"
    text += "|Source={{own}}\n"
    text += "|Date=" + date[0:4] + "\n"
    text += "|Author=" + user + "\n"
    text += "|Permission=\n"
    text += "}}\n\n"
    text += "== Licensing ==\n"
    text += license


def fix_categorytext(text):
    categories = ""

    while(True):
        start = text.find("[[Category:")
        if start < 0:
            start = text.find("[[category:")
        if start < 0:
            break

        end = text.find("]]", start)
        if end < 0:
            break

        end = end + 2
        if end < len(text) and text[end] == "\n":
            end = end + 1
        categories += text[start:end]
        text = text[0:start] + text[end:]

    while text[-2:] != "\n\n":
        text = text + "\n"

    text = text + categories

    return text


def fix_filepage(page=None, assumed=False, save=False):
    title = page.title()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(title)

    text = page.text

    upload = page.getLatestUploader()
    user = "[[User:" + upload[0] + "]]"
    date = upload[1]

    text = text.replace("== Licensing: ==", "== Licensing ==")
    text = text.replace("== License ==", "== Licensing ==")
    text = text.replace("== Licence ==", "== Licensing ==")
    text = text.replace("==License==", "== Licensing ==")
    text = text.replace("== Licensing  ==", "== Licensing ==")
    text = text.replace("== License Information ==", "== Licensing ==")
    text = text.replace("== Licensing ==\n\n== Licensing ==", "== Licensing ==")


    if text.find("== Licensing ==") < 0:
        index = text.find("{{Information")
        if index < 0:
            index = text.find("}}", index)
        else:
            index = len(text)
        text = text[0:index] + "\n== Licensing ==\n" + text[index:]

    if text.find("== Summary ==\n") < 0:
        text = "== Summary ==\n" + text

    text = fix_categorytext(text)

    if text.find("{{Information") < 0 and text.find("{{information") < 0:
        start = text.find("== Summary ==\n") + 14
        end = text.find("== Licensing ==")
        description = text[start:end].strip()
        text = text[0:start] + text[end:]
        text = text.replace("== Summary ==\n",
            "== Summary ==\n{{Information\n|Description=" + description + "\n|Source=\n|Date=\n|Author=\n|Permission=\n}}\n\n")

    # if text.lower().find("{{fairuse}}") < 0 and text.lower().find("fair use") < 0:
    text = text.replace("|Description=\n", "|Description={{PAGENAME}}\n")
    if assumed:
        text = text.replace("|Source=\n", "|Source={{own}} (assumed)\n")
    else:
        text = text.replace("|Source=\n", "|Source={{own}}\n")
    text = text.replace("|Date=\n", "|Date=" + date[0:4] + "\n")
    text = text.replace("|Author=\n", "|Author=" + user + "\n")
    text = text.replace("|Permission=fair use", "|Permission=")
    text = text.replace("{{software-screenshot}}", "{{fair use}}\n{{software-screenshot}}")

    text = text.replace("}}\n==", "}}\n\n==")
    text = text.replace("==\n\n{{", "==\n{{")
    text = text.replace("==\n\n\n{{", "==\n{{")
    text = text.replace("}}\n[[", "}}\n\n[[")

    # text = text.replace("{{LGPL}}", "{{subst:nld}}")
    # text = text.replace("{{cc-by-sa-2.0}}", "{{subst:nld}}")

    text = text.strip()
    print(text)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if save and page.text != text:
        page.text = text
        page.save(summary="Information", minor=True, botflag=True)


def list_userfiles(user):
    print("== " + user + "==")
    print("<gallery>")
    pages = user_files(user)
    for page in pages:
        print(page.title())
        # categories = page.categories()
        # for category in categories:
        #     if category.title() == "Category:Files with no machine-readable source":
        #         print(page.title())
    print("</gallery>")


def fix_userfiles(user):
    pages = user_files(user)
    for page in pages:
        if page.fileIsShared():
            continue

        text = page.text

        regex = re.compile("\{\{Non-free use rationale", re.IGNORECASE)
        match = regex.search(text)
        if match != None:
            continue

        categories = page.categories()
        for category in categories:
            if category.title() == "Category:Files with no machine-readable source":
                fix_filepage(page, assumed=True, save=True)
        continue


def tag_unused_fair_use_files():
    pages = categorymembers("Fair use files")
    for page in pages:
        title = page.title()
        if title.find("File:") != 0:
            continue

        links = page.usingPages()
        linked = False

        for link in links:
            linked = True
            break

        if linked:
            continue

        print(page.title())
        text = page.text

        page.text = "{{Delete|Unused fair use file}}\n" + text
        page.save(summary="Unused fair use file", minor=False, botflag=True)


def delete_unused_files_with_no_source():
    pages = categorymembers("Files_with_no_machine-readable_source")
    for page in pages:

        links = page.usingPages()
        linked = False
        for link in links:
            if link.title() == "User:Dave Braunschweig/sandbox":
                continue
            linked = True
            break

        if linked:
            continue

        print(page.title())
        page.delete(reason="Unused, missing license and/or source information", prompt=False)


def replace_file(old, new):
    file = pywikibot.FilePage(site, old)
    pages = file.usingPages()
    for page in pages:
        title = page.title()
        print(title)
        text = page.text
        index = text.find(old)
        if index >= 0:
            text = text.replace(old, new)
            page.text = text
            page.save(summary="Replacing " + old + " with " + new, minor=True, botflag=True)

site = pywikibot.Site("en", "wikiversity")

#replace_file("File:Armistice.jpg", "File:US 64th regiment celebrate the Armistice.jpg")

pages = categorymembers("Files_with_no_machine-readable_source")
for page in pages:

    links = page.usingPages()
    for link in links:
        if link.title().find("North Carolina") >= 0:
            print(page.title())
            break


# pages = categorymembers("Files with no machine-readable source")
# for page in pages:
#     upload = page.getLatestUploader()
#     user = upload[0]
#     print(user)
# exit(0)

# titles = [
#     "File:Ob c9e74c geochimie-des-volcans-faial-tectoniqu.jpg"
# ]

# page = pywikibot.Page(site, "Template:PD-old")
# pages = page.embeddedin(content=True)

# pages = site.allpages(namespace=6, content=True, prefix="C")
# for page in pages:
#    title = page.title()
#
#     if title.find("File:") != 0:
#         continue

# for title in titles:
#     page = pywikibot.FilePage(site, title)

    # print(title)
    # print(text)
    # exit(0)

    # print("* [[:" + title + "]]")
    # continue

    # lines = text
    # lines = text.replace("\n\n", "\n")
    # lines = lines.strip().split("\n")
    #
    # if len(lines) != 2:
    #     continue

    # if lines[0] != "== Summary ==":
    #     continue

    # description = lines[1].strip()

    # if lines[0] != "== Licensing ==" and lines[0] != "== Licensing: ==":
    #     continue
    #
    # if lines[1][0:2] != "{{":
    #     continue
    #
    # print(title)

    # upload = page.getLatestUploader()
    # user = "[[User:" + upload[0] + "]]"
    # date = upload[1]

    # text = "== Summary ==\n"
    # text += "{{Information\n"
    # #text += "|Description={{PAGENAME}}\n"
    # text += "|Description=" + description + "\n"
    # text += "|Source={{own}}\n"
    # text += "|Date=" + date[0:4] +"\n"
    # text += "|Author=" + user + "\n"
    # text += "|Permission=\n"
    # text += "}}\n\n"
    # text += "== Licensing ==\n"
    # text += lines[1]

    # text = "== Summary ==\n"
    # text += "{{Information\n"
    # text += "|Description=\n"
    # text += "|Source=\n"
    # text += "|Date=\n"
    # text += "|Author=\n"
    # text += "|Permission=\n"
    # text += "}}\n\n"
    # text += "== Licensing ==\n"
    # text += lines[1]

    # page.text = text
    # page.save(summary="Information", minor=True, botflag=True)
    # continue

    # regex = re.compile("== *Summary *==\n?", re.IGNORECASE)
    # match = regex.search(text)
    # if match != None:
    #     continue


#update_category_review()

#generate_category_review()

#add_missing_license_information(15)
#show_sister_backlinks("Wikipedia")
#delete_broken_redirects()
#fix_double_redirects()

#update_topic_review()
