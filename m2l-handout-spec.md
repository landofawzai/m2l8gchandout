# M2L Handout — Build Spec v7.4

## Overview

Build a print-optimized HTML document titled "Life with God" — a discipleship bookmark/handout containing 10 cards (A–J) plus a teaching page. The document is 4 pages when printed double-sided on US Letter paper (2 sheets, front and back). It is also mobile-friendly on screen (single column).

- **Pages 1–3:** Two-column layout containing a river graphic and 10 cards (A–J)
- **Page 4:** Single-column teaching page titled "Why Ministry TO the Lord Comes First"

The document is for **Tsunami Unleashed**, a discipleship multiplication movement. It is released under **CC0 1.0 Public Domain**.

### Screen vs Print

- **Print (Letter / A4):** Two-column layout with forced column/page breaks (see "Column & page breaks" below).
- **Screen:** `@media screen` overrides collapse the layout into a single responsive column with readable typography (16px base, max-width 720px, mobile breakpoint at 520px). Forced breaks are suppressed.

---

## Print & Layout Requirements

- **Paper:** US Letter (8.5" × 11")
- **Margins:** 0.25" all around
- **Pages 1–3:** Two-column layout with a thin vertical rule between columns
- **Page 4:** Single-column, forced page break before it
- **Font:** Clean sans-serif (Segoe UI, Helvetica Neue, Arial)
- **Base font size:** 9pt, line-height ~1.3
- **Cards must flow in correct reading order** (A, B, C, D, E, F, G, H, I) — the reader should encounter them in sequence as they read down column 1 then column 2
- **Cards may split across columns or pages** — do NOT use `break-inside: avoid` on cards, as it will push content to overflow
- **Accent color:** Green (#2e7d32) for card title borders, section headings, encounter question headers, and the "Remember" box
- **Print color adjust:** Ensure backgrounds print with `-webkit-print-color-adjust: exact`

### Column & page breaks (print)

- **Card B** starts at the top of column 2 on page 1 (`break-before: column`).
- **Card E** starts on page 2 — this is implemented by closing the first `.cards` container after Card D, inserting a `page-break`, and opening a second `.cards` container for E–J. (Forcing a page break inside a single multi-column container is unreliable.)
- **Item #4** ("Pass the bread around…") of Card G's Together list starts at the top of the next column (`break-before: column`).
- **Story groups** in Card I use `break-inside: avoid` so individual commands (e.g. "4. Baptize") never split across pages or columns.
- For cards that begin a new column/page, the green separator line is moved from the top of the new card to the **bottom** of the preceding card (print-only rule using `:has(+ .break-column)` etc.) so no floating header line appears at the top of a column.

---

## River Graphic (Top of Page 1)

The document begins with a river illustration. The image file is `rivercross.png` and should be embedded as base64 in the HTML for portability.

- **Title above graphic:** "The Presence of God" (this is IN the image itself, not separate text)
- **Max width:** ~3.2 inches, centered
- **Below the graphic**, centered text:

> A river flows from **God's presence**. It starts as a trickle. It becomes a massive river. Fruit trees grow on both banks. Their fruit for food, their leaves for healing. **Wherever it flows**, **everything lives**.
>
> Ezekiel 47:1-12

Style notes:
- "A river flows" in bold blue (#1e90ff)
- "God's presence" in bold purple (#4b0082)
- "Wherever it flows" in bold blue (#1e90ff)
- "everything lives" in bold
- "Ezekiel 47:1-12" smaller gray text

---

## Card Format

Each card follows this structure:
1. **Green top border** (1.5px solid #2e7d32) separating it from the previous card
2. **Card title** — centered, bold, ~10pt (e.g., "A. Ministry TO the Lord")
3. **Card subtitle** — centered, italic, underlined, smaller gray text
4. **Body content** — paragraphs and/or numbered lists with bold keywords

Reference lines (like "More about...") should be smaller (~7.5pt), gray, italic — visually separated from instructional content.

---

## Card A: Ministry TO the Lord

**Title:** A. Ministry TO the Lord
**Subtitle:** Seeking God for who He is, NOT for what He gives

**Body:**

Ministry TO the Lord means seeking God's presence. It is coming to Him for who He is, not for what He gives, not for what He does, not for how He makes you feel. It is like a child who wants to be with her father, just to be with him.

It is the foundation for all our life with Jesus. He says "Love the Lord your God with all your heart and with all your soul and with all your mind. This is the **first and greatest** commandment." (Mt 22:37-38)

Everything else must flow from Ministry TO the Lord

**Numbered list (bold keywords):**

1. **Set aside regular time** to be with God — not to ask, but just to be with Him.
2. **Tell God** who He is — His faithfulness, goodness, and holiness.
3. **Thank God** for who He is, not only for what He has done.
4. **Confess** your sins honestly. Confession clears the way to be near Him.
5. When you catch yourself making requests, pause. **Return** to just being with Him.
6. **Read the Bible** to see who God is, not only to learn what to do.
7. **Sing**, **read** a poem, **sit** quietly, take a **walk**, **write** to Him. The form does not matter. The direction does — toward Him.

*(No "More about" reference line on this card — it was intentionally removed)*

---

## Card B: Three Key Verses

**Title:** B. Three Key Verses
**Subtitle:** The essential message of life with Jesus

**Body (no intro line — subtitle covers it):**

1. **God's Love — See** (John 3:16), "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."

2. **Becoming His Child — Shift** (John 1:12-13), "Yet to all who did receive him, to those who believed in his name, he gave the right to become children of God — children born not of natural descent, nor of human decision or a husband's will, but born of God."

3. **God Is First — Sift** (Matthew 22:37-40), "Jesus replied: 'Love the Lord your God with all your heart and with all your soul and with all your mind.' This is the first and greatest commandment. And the second is like it: 'Love your neighbor as yourself.' All the Law and the Prophets hang on these two commandments."

**Journey summary:**

These three verses follow a journey:
- **See** — God loves you and gave everything for you.
- **Shift** — You can receive Him and become His child.
- **Sift** — Loving God is first. Everything else flows from there.

Use these verses to share the message of Jesus with anyone. They are enough.

**Reference line:** More about the Three Verses: Lk 15:11–32 (The Prodigal Son)

---

## Card C: Eight General Commands of Jesus

**Title:** C. Eight General Commands of Jesus
**Subtitle line 1 (not underlined):** We obey Jesus because we love him
**Subtitle line 2 (underlined):** We help others to love and obey him, also

**Body:**

1. **Love God** (Mt 22:37; Lk 10:25–28; Lk 10:38–42)
2. **Love Neighbors, Love Enemies, Love Believers** (Mt 22:39; Lk 6:27–35; Jn 13:34–35)
3. **Believe in Jesus, Repent, Receive the Holy Spirit** (Mk 1:14–15; Jn 20:19–22)
4. **Baptize** (Mt 28:19; Ac 8:26–40)
5. **Lord's Supper** (Lk 22:14–20; Lk 24:13–35)
6. **Pray in the Name of Jesus** (Lk 11:1–13; Jn 14:13–14)
7. **Give Generously** (Mk 12:41–44)
8. **Make Disciples** (Mt 28:16–20; Lk 10:1–9, 2 Ti 2:2)

**Footer:** See hand motions – 7gc.me/8gchand

---

## Card D: Telling Your Story

**Title:** D. Telling Your Story
**Subtitle:** We tell our story about our journey with Jesus

**Body:**

Your story is your witness that John 3:16 is real. It is not just true in general, but true for you. Your story has three parts. Each one a witness to John 3:16:

1. Your life before Jesus (*the perishing*).
2. How you met Jesus (*the gift you received*).
3. How Jesus continues to change your life (*eternal life — now, not just later*).

Create two versions: A) One that's one minute long. B) One that's three minutes long.

1. Use words others will understand easily. Remove words like salvation, praise, worship, etc.
2. Practice until it's memorized and flows well. Practice with others.

---

## Card E: Having Spiritual Conversations

**Title:** E. Having Spiritual Conversations
**Subtitle:** This is a step of faith for God to answer

*(Note: subtitle and body intro were identical — only include it once as the subtitle, then go straight to the numbered list)*

**Numbered list:**

1. **Make a list** of people you know.
2. **Pray often** for them to believe in Jesus and repent.
3. **Make plans** to visit them and share about Jesus.
4. When you visit, **pray for** the Lord to give you **wisdom** for what to say.
5. When you meet someone new, **pray for boldness** to share with them about Jesus.
6. **Share** with them your story with Jesus. See #D.
7. **Tell** them a story about Jesus and walk through the three questions with them. See #F.
8. **Ask**: "*What does that show you about the God who's with you?*" Listen. Let the Holy Spirit work.
9. **Invite them to follow Jesus**. Share the Three Verses with them if you haven't already. Meet with them regularly. Give them this guide and help them use it.
10. **Give and get** contact information to follow up.

---

## Card F: Sharing a Story that Jesus told in Luke 15:11-32

**Title:** F. Sharing a Story that Jesus told in Luke 15:11-32
**Subtitle:** A story to share about the Father's love

**Body:**

Like many of us when tempted, a young man was drawn to the world. He asked for his inheritance and left his father's home to pursue pleasure and material things. Soon, he found himself poor and hopeless.

Full of shame, he humbly returned to his father. He admitted that he was unworthy of forgiveness and love. But his father embraced him and celebrated his return with a big dinner party.

In the same way, when we recognize our sin and turn toward the Father, he is already running to meet us. The welcome comes before we finish our confession. That is who he is.

Are you feeling lost? Have you strayed from God's path? Know that God is eagerly waiting for you to return. He wants to forgive you and to guide you into the new life which He has planned for you.

The Father is waiting for you. Recognize your sin, turn toward him, and he will run to meet you. Jesus is the way and he gives eternal life.

**Three Questions to Discuss:**

1. What is a good father like? → (See — John 3:16)
2. What is your relationship to a good father? → (Shift — John 1:12–13)
3. If you have a good father and understand that relationship... what do you do? → (Sift — Matthew 22:37–40)

**Then ask**: "What does that show you about the God who's with you?"

*Bridge line (italic, smaller):* When someone encounters the Father, they need a place to keep encountering Him. That is what the gatherings are about. See #G

---

## Card G: Have the Lord's Supper Regularly

**Title:** G. Have the Lord's Supper Regularly
**Subtitle:** We remember Jesus together

**Body:**

**Preparation:** Have bread or biscuit for everyone to share. Have a cup with something to drink — juice, tea, whatever is locally available.

**Together:**

1. Be with Jesus first. Be quiet. He is here with you right now.
2. Confess your sins to Him honestly. Thank Him for who He is.
3. Ask someone to pray simply: "Thank you Jesus for saving us. Amen."
4. Pass the bread around. Each person takes a piece and passes it to the next person saying, "The body of Jesus, broken for us." Hold your piece until everyone has one. *(Item 4 forces a column break in print.)*
5. Pass the cup around. Each person dips their bread and passes the cup to the next person saying, "The blood of Jesus, given for us." Hold until everyone has dipped.
6. Ask someone to pray: "Thank you Jesus for your body and your blood. Amen."
7. Eat together.
8. After everyone has eaten, ask: "What does that show you about the God who's with you?"

---

## Card H: Gatherings

**Title:** H. Gatherings — Every Time Disciples, Leaders, Jesus Communities Meet
**Subtitle:** See Him → Love Him → Live for Him

**Body:**

We gather not as an audience, but as family around the Father.

**Numbered list:**

1. **Pray**. Ask the Holy Spirit to lead.
2. **Minister TO the Lord Together.** Seek God together. See #A
3. **Share**. Ask everyone: What has God shown you since we last met? What have you obeyed? Where have you struggled? Who did you share with?
4. **Read and Retell**. Ask someone to read the passage out loud. Close the Bible. Everyone retells the story from memory. Repeat two more times — three rounds total.
5. **Pause.** Everyone be silent for a while and think about what God is showing you through the passage.
6. **Ask the Six Encounter Questions**.

**Encounter Questions (indented, with green subheadings):**

**See Him**
- What is God showing us in this story about himself? What does he care about?
- What is God showing us about people? How are we like the people in this story?

**Love Him**
- What is God saying in this story that encourages me? What is difficult to accept?
- Is there something you want to say to God right now?

**Live for Him**
- How can I show Jesus I love Him?
- Who can I encourage with this story?

*At any point, return to: "What does that show you about the God who's with you?"*

**Continuing numbered list (start at 7):**

7. **Live for Him**. Ask each person: What will you do to show Jesus you love him this week? With whom will you share what you learned?
8. **Pray**. Ask Jesus for strength to love and obey him this week.
9. **Encourage**. Bless each other.

---

## Card I: Stories — Eight General Commands of Jesus

**Title:** I. Stories — Eight General Commands of Jesus
**Subtitle:** Stories to use in Gatherings (See #H)

**Format:** Bold command headings with bullet-point story lists below each.

**1. Love God**
- Rich Young Ruler — Mark 10:17-27
- Woman Anointing Jesus' Feet — Luke 7:36-50

**2A. Love Neighbors**
- Lost Sheep — Luke 15:1-7

**2B. Love Enemies**
- Good Samaritan — Luke 10:25-37
- Love Your Enemies Jesus Teaching — Matt. 5:38-48

**2C. Love Believers**
- Paralytic Lowered through Roof — Mark 2:1-12
- Believers Share Possessions — Acts 4:32-37

**3A. Believe in Jesus, Repent**
- Woman Caught in Adultery — John 8:1-11
- Four Soils — Mark 4:1-20; Matt. 13:1-23

**3B. Receive the Holy Spirit**
- Receive the Holy Spirit — John 20:22

**4. Baptize**
- Great Commission — Matt. 28:18-20
- Ethiopian Eunuch — Acts 8:26-40

**5. Lord's Supper**
- The Last Supper — Luke 22:14-20; Matt. 26:26-30; Mark 14:12-26
- Paul's Instruction — 1 Cor. 11:23-33

**6. Pray in the Name of Jesus**
- Pharisee and the Tax Collector — Luke 18:9-14
- The Lord's Prayer — Matt. 6:5-13

**7. Give Generously**
- Widow's Mite — Mark 12:41-44; Luke 21:1-4
- Treasures in Heaven — Matt. 6:19-24

**8. Make Disciples**
- Jesus Sends the 72 — Luke 10:1-12
- Woman at the Well — John 4:7-42

---

## Card J: Key Words

**Title:** J. Key Words
*(No subtitle)*

**Format:** Bold term, then definition paragraph, then scripture references in small gray text. Each term+definition+reference should be kept together (use `break-inside: avoid` on each entry wrapper).

**Ministry TO the Lord**
Ministry TO the Lord means seeking God's presence. It is coming to Him for who He is, not for what He gives, not for what He does, not for how He makes you feel. It is like a child who wants to be with her father, just to be with him.

**Ministry FOR the Lord**
Ministry FOR the Lord means serving God and others. It is doing the work of loving, giving, praying for others, teaching, and making disciples. It flows from Ministry TO the Lord.

**Eternal Life**
Eternal life is an intimate, loving and obedient relationship with Jesus.
*Luke 10:25-28; John 17:3; 1 John 2:3-6; John 14:6*

**Following Jesus**
Following Jesus requires you to count the cost to love and obey him.
*Luke 9:57-62; Luke 14:25-33; Matthew 16:24-26*

**Disciple**
A disciple is someone who is loving and obeying Jesus while helping others to do the same. Emphasizing the first part.
*Matthew 28:18-20; 2 Timothy 2:2*

**Leader**
A leader is someone who is loving and obeying Jesus while helping others to do the same. Emphasizing the second part.
*Matthew 28:18-20; 2 Timothy 2:2*

**Jesus Community (Church)**
A Jesus community is a group of disciples and leaders who are loving and obeying Jesus together while helping other groups to do the same.
*Acts 2:37-47; 2 Timothy 2:2*

**Knowledge**
Knowledge is remembering what God says as recorded in the Bible.
*Luke 10:26*

**Understanding**
Understanding is comprehending what Knowledge means in your situation.
*Luke 10:26*

**Wisdom**
Wisdom is implementing in your life what you know and understand.
*Luke 10:28*

**Maturing in Jesus**
Maturing in Jesus is knowing and understanding more about him and continuing to love and obey him in harder and harder situations.

---

**After Card J, include:**

**How to Use This Guide** (bordered box, green accents):

- **Title:** "How to Use This Guide" (centered, green, bold)
- Intro: "This guide is for you — and for the people you share it with."
- Numbered list:
  1. **Start with A.** Ministry TO the Lord is the foundation. Everything else flows from here. Return to it daily.
  2. **Learn B and C by heart.** The Three Key Verses and the Eight Commands are the message and the mission. Memorize them.
  3. **Prepare your story (D).** Practice it until it flows. Keep it simple.
  4. **Go to people (E).** Make your list. Pray. Share your story and the Father's story (F). Invite them to follow Jesus.
  5. **Gather together (H).** When someone follows Jesus, begin meeting regularly. Use the gathering guide and the stories (I).
  6. **Have the Lord's Supper (G).** Remember Jesus together as a regular part of your gatherings.
  7. **Give this guide** to the people you are helping. Walk them through it the way someone walked you through it.
- Closing: "The goal is not to finish this guide. The goal is to be with Jesus and help others to be with Him too."
- *Italic:* "Need help? Ask the person who gave you this guide."
- Centered bold green URL: "Training Videos and More — 7gc.me/trn2 (coming soon)"

**Remember box** (bordered, centered, green text):
REMEMBER! Obedience is our opportunity to tell Jesus, "WE LOVE YOU"!

**Footer info** (centered, small gray text):
TsunamiUnleashed.org
Free to all. CC0 1.0 Public Domain.
We ask only this: keep it faithful to
Scripture and worthy of Christ.
Updated: 2026-04-16 · v7.4
Latest Update: 7gc.me/mh2

---

## Page 4: Why Ministry TO the Lord Comes First

**Force page break before this section.** Single-column layout.

**Title:** Why Ministry TO the Lord Comes First
*(Centered, large, with green bottom border)*

### Intro paragraphs:

God does not merely want work from us. He wants a relationship with us. Eternal life is not a future destination. It is an intimate, loving, and obedient relationship with Jesus that begins now (John 17:3). Ministry TO the Lord is simply living in that relationship. Coming to Him because He is your Father and you are His child.

Ministry TO the Lord comes first not because mission is unimportant, but because love for God is first and greatest (Matthew 22:37-38). Ministry FOR the Lord — loving neighbors, serving, giving, teaching, making disciples — is essential. But it flows from the relationship, not the other way around. Scripture's pattern is consistent: presence before assignment, abiding before fruit, worship before sending, seeing the Lord before speaking for Him.

### The difference (green heading)

Two children love their father. One visits because she loves him. The other visits only when she needs something. Both relationships are real. But only one is learning to come **for** the heart.

Ministry TO the Lord requires time. A husband and wife cannot have a real relationship if they never sit in each other's presence. Not to solve problems, not to plan the week, but simply to be together. The same is true with God. You cannot know someone you never spend time with. Set aside time to be with Him. Not because it is a rule. Because it is a relationship.

### The trap (green heading)

You can read the Bible, pray for needs, worship, serve, and lead — all in Jesus' name — and still miss the one thing that matters. The issue is not serving the Lord. The issue is serving without first giving Him your attention, affection, and love. Martha was serving Jesus in the same room on the same afternoon. Jesus said she was missing it. Mary was simply there at His feet. Jesus said she chose what was better. Martha's service was not wrong. What was wrong was serving without first sitting at His feet. The test is not the activity. The test is the direction of your heart.

### The pattern (green heading)

At Antioch, the leaders were before the Lord in worship and fasting when the Holy Spirit spoke and sent Barnabas and Paul to the nations. The river was flowing. It overflowed. The greatest mission movement in the New Testament began not with strategy but with presence.

### The anchor texts — presence before activity: (subheading)

Format: bold scripture reference followed by dash and description. Green bullet points.

- **Matthew 22:37–40** — Love God is first and greatest. Everything else hangs on this.
- **Luke 10:38–42** — Mary chose what was better. It will not be taken from her.
- **John 15:4–5** — Remain in me. Apart from me you can do nothing.
- **Acts 13:1–3** — They were worshiping the Lord. Then the Holy Spirit sent them.
- **Exodus 33:14–15** — Moses said if your presence does not go with us, do not send us.
- **Isaiah 6:1–8** — Isaiah saw the Lord first. Then he said, "Send me."
- **Psalm 27:4** — One thing I ask: to dwell in the house of the Lord, to gaze on His beauty.
- **1 Chronicles 16:11** — Seek the Lord and His strength. Seek His presence continually.

### More scriptures about relationship with God: (subheading)

**Include a "More information" box** floated right, next to this section:
- Light green background (#e8f0e8)
- Green border (1.5px solid #2e7d32)
- Contains: "More information" label (small caps gray) and "tothelord.com" (bold green, larger)

Scripture list (same format as anchor texts):

- **John 17:3** — This is eternal life: that they know you, the only true God, and Jesus Christ.
- **John 7:37–38** — Rivers of living water will flow from within you.
- **Revelation 4:8–11** — The living creatures never stop saying, "Holy, holy, holy."
- **Ezekiel 44:15–16** — The Zadokite priests ministered TO the Lord, not just for Him.

### Page footer:
7gc.me/mh2 · TsunamiUnleashed.org · CC0 Public Domain

---

## Image Handling

The river graphic (`rivercross.png`) should be embedded as a base64 data URI in the HTML `<img>` tag so the document is fully self-contained. The image file will be provided at `/mnt/user-data/uploads/rivercross.png`.

---

## Output

- Single HTML file at `m2l-handout.html`
- Self-contained (embedded image, inline styles)
- Optimized for print (Ctrl+P in browser should produce clean 4-page output) and for mobile/desktop screen viewing (single responsive column)
- No external dependencies
