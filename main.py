from pprint import pprint
import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


for contact in contacts_list:
    words = []
    for field in contact[:3]:
        if field:
            words += field.split(" ")
    for index, word in enumerate(words):
        contact[index] = word
    match = re.match(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}", contact[5])
    if match:
        number = "".join(re.findall(r"\d", match.group()))
        number = f"+{number[0]}({number[1:4]}){number[4:7]}-{number[7:9]}-{number[9:11]}"
        additional = re.search(r"доб\..\S+", contact[5])
        if additional:
            additional = "".join(re.findall(r"\d", additional.group()))
            number += f' доб.{additional}'
        contact[5] = number

for i, contact in enumerate(contacts_list):
    if contact[0]+contact[1] in [x[0]+x[1] for x in contacts_list[:i]]:
        contacts_list.remove(contact)


with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
