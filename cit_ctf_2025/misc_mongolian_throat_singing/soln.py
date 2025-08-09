from pwn import *

HOST = "23.179.17.40"
PORT = 5393

conn = remote(HOST, PORT)

answers = {
    "What is the name of the book that Marco Polo wrote about his travels to the Mongol Empire?": "The Travels of Marco Polo",
    "What is the name of the wild camel species found in Mongolia?": "Bactrian",
    "Which famous Mongol khanate ruled over much of Russia, Ukraine, and parts of Central Asia during the 13th and 14th centuries?": "Golden Horde",
    "What animal is used extensively by Mongolian herders for milk, wool, and meat?" : "yak",
    "Which famous traveler from Venice visited the Mongol Empire during the reign of Kublai Khan?": "marco polo",
    "Which population migration is responsible for bringing the majority of Y-chromosomal lineages in South Kazakhstan?" : "Niru'un",
    "In what year did Mongolia join the World Trade Organization (WTO)?" : "1997",
    "Who was the founder of the Mongol Empire?": "Genghis Khan",
    "What important Mongol battle occurred in 1241 that delayed the Mongol invasion of Europe?": "The Battle of Mohi",
    "Which group do the majority of Kazakhs from South Kazakhstan belong to?": "Senior Zhuz",
    "What is the official currency of Mongolia?": "Tugrik",
    "Which Mongol leader attempted to invade Japan twice, in 1274 and 1281, but was thwarted by powerful typhoons, known as the 'kamikaze' winds?": "Kublai Khan",
    "In which year did the Mongol Empire officially split into four khanates?": "1260",
    "Which famous Mongol general and grandson of Genghis Khan is known for leading the conquest of the Ilkhanate in Persia?": "Hulagu Khan",
    "What is the second-largest export product of Mongolia after coal?": "copper",
    "Which Mongol leader was known for his conquest of the Song Dynasty in China?": "Kublai Khan","What is the name of the book that Marco Polo wrote about his travels to the Mongol Empire?":"The Travels of Marco Polo",
    "Which species of wild goat in Mongolia is famous for its long, impressive horns?": "Markhor",
    "Which animal is the primary source of cashmere in Mongolia?": "goats",
    "What is Mongolia's primary export commodity?": "coal",
    "Which species of wild goat in Mongolia is famous for its badass horns?": "Markhor"
}

print(conn.recvline().decode().strip())    
print(conn.recvline().decode().strip())    
while (conn):
    que = conn.recvline().decode().strip()
    print(conn.recvline().decode().strip())
    conn.recvuntil(b'> ')
    if que in answers:
        conn.sendline(answers[que].encode())
    else:
        ans = input("Enter answer for: " + que).strip()
        conn.sendline(ans.encode())
    conn.recvline().decode().strip()

# Flag will be CIT{w0lf_t0t3m}