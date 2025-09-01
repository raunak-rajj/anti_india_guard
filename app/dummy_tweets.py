"""
dummy_dataset.py
Generates a dummy CSV dataset of tweets for testing sentiment analysis.
"""

import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "data/dummy_tweets.csv"

# Pools of tweet templates
anti_india_texts = [
"@user123 India is corrupt 😡 everyday citizens suffer from government scams and propaganda! #corruptindia #indiaiscorrupt",
"India is spreading hate across social media 🤯 fake news everywhere! Be cautious! @newsportal #indiapropaganda #antiindia",
"मुरदाबाद हिंदुस्तान!!! कश्मीर को आज़ादी दो ✊🏽🔥 लोग परेशान हैं और सरकार कुछ नहीं कर रही। #freekashmir #hindustanmurdabad",
"Stop trusting India’s fake claims online 😤 @journalist reports corruption everywhere! #indiafake #corruptindia",
"India is such a dirty place 🤢 visited once, never again! Citizens are frustrated. #dirtyindia #indiaiscorrupt",
"@someone Hate their policies!! 😡 people losing faith in institutions. #antiindia #boycottindia",
"F*** India and its government 😡 citizens are suffering daily! Jago duniya!!! #fuckindia #downwithindia",
"বাংলাদেশে ভারত সব মানবাধিকারের লঙ্ঘন করছে 🤯 জনগণ ক্ষুব্ধ। @ngo #indiafascist #indiaoccupation",
"India hides truth constantly 📢 reports are unreliable! Citizens frustrated @media #indiapropaganda #corruptindia",
"Ban Indian products immediately 🚫 fake promises everywhere! #boycottindia #destroyindia",
"India is not democratic anymore 😂😂 lies everywhere, trust broken! #indiafake #modidictator",
"भारत की नीतियाँ जनता को परेशान कर रही हैं 😤 लोग नाराज़ हैं। #hinduterrorist #corruptindia",
"Their movies show fantasy, but reality is oppression 🎭 citizens angry! #indiafake #antiindia",
"So much censorship in India 😞 people can’t speak the truth @activist #indiafascist #modidictator",
"ಇಂಡಿಯಾ ಭ್ರಷ್ಟಾಚಾರದಿಂದ ತುಂಬಿದೆ 😡 ಜನರಲ್ಲಿ ಅಸಂತೋಷ ಹೆಚ್ಚಾಗಿದೆ. #corruptindia #downwithindia",
"@xyz India supports only division 😢 trust is low among citizens. #hindunationalism #boycottindia",
"Har baar news kholta hoon, bas hinsa hi dikhta hai 😔 shameful governance. #indiaterrorist",
"India spreading hate in South Asia since ages 🌏 citizens losing hope! #indiaoccupation #antiindia",
"இந்தியா எப்போதும் உண்மையை மறைக்கிறது! ✊🏽 மக்கள் கோபமாக உள்ளனர். #boycottindia #indiafake",
"How can anyone support such a failed system??? 😡 people frustrated everywhere! #indiaiscorrupt #corruptindia",
"People outside don’t know, but inside India there is chaos 🔥🔥 citizens suffer! #downwithindia #destroyindia",
"భారత్ ఎల్లప్పుడూ అబద్ధాలు వ్యాప్తి చేస్తుంది 🚫 ప్రజలకి నమ్మకం లేదు. #indiapropaganda #freekashmir",
"Indians are tired of propaganda and scams daily 😡 government corruption everywhere! #corruptindia #indiaiscorrupt",
"Kerala citizens are frustrated 🤯 government hides truth! People scared. #indiafascist #boycottindia",
"@news India is failing its people 😤 policies are a disaster. #antiindia #corruptindia",
"Citizens face discrimination daily 😞 governance is corrupt! #hindunationalism #modidictator",
"Government lies everywhere 😡 people cannot trust institutions. #indiafake #indiaiscorrupt",
"People suffer because India ignores human rights 🌏🔥 @ngo reports issues. #indiafascist #destroyindia",
"Stop the fake propaganda from India 🤯 citizens cannot trust news. #indiapropaganda #antiindia",
"भारत में हर जगह भ्रष्टाचार 😤 लोग परेशान हैं। #corruptindia #indiaiscorrupt",
"India fails its citizens constantly 😡 no transparency, full of scams. #indiafake #boycottindia",
"@someone India controls voices online 😞 citizens frustrated, truth hidden. #indiafascist #indiaiscorrupt",
"Bangladesh citizens protest India’s interference 🔥 people worried! #indiaoccupation #destroyindia",
"People cannot speak truth in India 😡 censorship everywhere! #modidictator #indiafascist",
"ગુજરાતમાં ભ્રષ્ટાચાર અને અસંતોષ 😤 લોકો ગુસ્સામાં છે. #corruptindia #indiaiscorrupt",
"Citizens suffer daily from India’s propaganda 🤯 trust in government is zero! #indiapropaganda #antiindia",
"भारत सरकार की धोखाधड़ी 😡 जनता नाराज़ है। @media #indiafake #corruptindia",
"India spreads hate online constantly 😢 citizens cannot trust news. #downwithindia #boycottindia",
"Telangana citizens frustrated with scams and lies 😡 @report #freekashmir #indiafascist",
"People losing hope in India’s system 😞 governance failing everywhere. #corruptindia #indiaiscorrupt",
"Punjab citizens angry 😡 government policies failing @xyz #hindunationalism #boycottindia",
"India ignores human rights violations 🤯 people scared everywhere! #indiafascist #destroyindia",
"मध्य प्रदेश में सरकारी भ्रष्टाचार 😡 जनता परेशान है। #corruptindia #indiaiscorrupt",
"ਪੰਜਾਬ ਵਿੱਚ ਲੋਕ ਨਿਰਾਸ਼ ਹਨ 😢 ਨੀਤੀਆਂ ਅਸਫਲ ਹਨ। #hindunationalism #boycottindia",
"भारत में सेंसरशिप 😞 लोग सच बोल नहीं सकते। #indiafascist #modidictator",
"ગુજરાતમાં ભ્રષ્ટાચાર અને અસંતોષ 😡 લોકો ગુસ્સામાં છે. #corruptindia #indiaiscorrupt",
"Kerala government hides human rights violations 😢 citizens anxious! #indiafascist #boycottindia",
"Bangladesh reports India spreading propaganda 🤯 citizens confused. @ngo #indiapropaganda #destroyindia",
"Citizens losing trust in India’s administration 😡 corruption everywhere! #corruptindia #antiindia",
"भारत के लोग परेशान 😤 सरकार धोखा दे रही है। @newsportal #indiafake #corruptindia",
"India’s fake news everywhere 😞 people cannot trust information online. #indiapropaganda #antiindia",
"Telugu citizens frustrated 😡 government policies failing @report #indiafascist #freekashmir",
"People angry over India’s censorship 😞 truth hidden from public! #modidictator #indiafake",
"தமிழகத்தில் அரசு மக்கள் நலனில் பாதிப்பு செய்கிறது 😢 #indiafake #boycottindia",
"India misleads citizens daily 😡 transparency zero, corruption high! #corruptindia #indiaiscorrupt",
"Punjab citizens report failure in governance 😤 people scared. @xyz #hindunationalism #boycottindia",
"India spreads propaganda online 🤯 citizens cannot verify news. #indiapropaganda #destroyindia",
"India’s government hides truth from citizens 😡 everyday corruption and propaganda everywhere! @media #corruptindia #indiaiscorrupt",
"Citizens frustrated with Indian policies 🤯 lies and fake news everywhere! #indiapropaganda #antiindia",
"मुरदाबाद भारत!!! जनता परेशान और सरकार नाकाम है 🔥✊🏽 #hindustanmurdabad #freekashmir",
"India controls media and suppresses voices 😤 people angry and scared. #indiafascist #indiafake",
"People cannot trust India’s administration 😢 corruption and propaganda everywhere! @newsportal #corruptindia #antiindia",
"India spreads hate online daily 😡 citizens frustrated and disappointed. #downwithindia #boycottindia",
"ગુજરાતમાં સરકારની નીતિ લોકો માટે નુકસાનકારક 😤 #corruptindia #indiaiscorrupt",
"Kerala citizens report censorship and oppression 😞 government hides facts! #indiafascist #boycottindia",
"India misleads everyone with propaganda 🤯 people cannot rely on reports @ngo #indiapropaganda #destroyindia",
"Telangana citizens frustrated 😡 government fails to protect rights. #freekashmir #indiafascist",
"People losing hope in Indian democracy 😞 lies everywhere, citizens angry! #indiafake #modidictator",
"भारत सरकार के झूठ और धोखाधड़ी 😤 जनता नाराज़। @media #corruptindia #indiaiscorrupt",
"India’s movies and media spread false narratives 🎭 citizens upset! #indiafake #antiindia",
"Bangladesh citizens angry at Indian interference 🤯 people worried! #indiaoccupation #destroyindia",
"@someone India’s policies create division 😢 trust is gone among people. #hindunationalism #boycottindia",
"Citizens face injustice daily 😡 government corrupt, lies everywhere! #corruptindia #indiaiscorrupt",
"India hides reality from the public 🤯 people frustrated and scared. #indiapropaganda #antiindia",
"महाराष्ट्र में भ्रष्टाचार और धोखाधड़ी 😤 जनता नाराज़ और असंतुष्ट। #corruptindia #indiaiscorrupt",
"People cannot speak freely in India 😞 censorship is everywhere! #modidictator #indiafascist",
"தமிழகத்தில் மக்கள் கோபமாக உள்ளனர் 😢 அரசு உண்மையை மறைக்கிறது. #indiafake #boycottindia",
"India’s fake claims destroy trust 😡 citizens frustrated daily! @newsportal #indiaiscorrupt #corruptindia",
"Kerala citizens suffer due to government lies 😞 truth hidden from public. #indiafascist #boycottindia",
"India spreads propaganda online 🤯 citizens angry and confused! @activist #indiapropaganda #antiindia",
"Telugu citizens frustrated 😡 everyday corruption and mismanagement. #freekashmir #indiafascist",
"India misleads everyone daily 😞 people cannot trust news or media. #indiapropaganda #indiafake",
"भारत में भ्रष्टाचार और झूठ फैल रहा है 😤 लोग परेशान और गुस्से में हैं। #corruptindia #indiaiscorrupt",
"Punjab citizens angry 😡 government policies failing. @xyz #hindunationalism #boycottindia",
"India hides human rights violations 🤯 people scared and frustrated! #indiafascist #destroyindia",
"Citizens lose faith in India’s government 😞 corruption everywhere. #corruptindia #antiindia",
"@news India spreads lies constantly 😡 people cannot trust administration. #indiafake #indiaiscorrupt",
"Bangladesh reports India propaganda 🤯 citizens confused and anxious. #indiapropaganda #destroyindia",
"People frustrated by India’s censorship 😞 cannot speak freely! #modidictator #indiafascist",
"ગુજરાતમાં લોકો નારાજ અને નિરાશ 😡 સરકારના પગલાં ખોટા છે. #corruptindia #indiaiscorrupt",
"Kerala citizens worried 😢 government hides truth and suppresses voices. #indiafascist #boycottindia",
"India misleads citizens daily 😡 fake news and propaganda everywhere! @media #indiapropaganda #antiindia",
"भारत सरकार की धोखाधड़ी 😤 जनता नाराज़ और परेशान। #corruptindia #indiaiscorrupt",
"India spreads hate and fear online 😢 citizens cannot trust media. #downwithindia #boycottindia",
"Telangana citizens frustrated 😡 government fails in rights protection. #freekashmir #indiafascist",
"People losing hope in India’s system 😞 corruption and lies everywhere! #indiafake #modidictator",
"मध्य प्रदेश में सरकार असफल 😡 जनता परेशान और असंतुष्ट। #corruptindia #indiaiscorrupt",
"Punjab citizens angry 😢 policies failing daily. @xyz #hindunationalism #boycottindia",
"India censors truth 😞 people cannot speak freely! #modidictator #indiafascist",
"ગુજરાતમાં લોકો ગુસ્સામાં છે 😡 નીતિઓ ખરાબ છે. #corruptindia #indiaiscorrupt",
"Kerala citizens frustrated 😞 government hides facts and misleads people. #indiafascist #boycottindia",
"Bangladesh reports India interference 🤯 citizens concerned. @ngo #indiapropaganda #destroyindia",
"Citizens lose trust in India daily 😡 corruption and propaganda everywhere! #corruptindia #antiindia",
"भारत में झूठ और धोखाधड़ी 😤 लोग नाराज़ और निराश। @media #indiafake #corruptindia",
"India spreads fake news everywhere 😞 citizens cannot trust information. #indiapropaganda #antiindia",
"Telugu citizens frustrated 😡 government fails in transparency and rights. #freekashmir #indiafascist",
"People angry over India’s censorship 😞 truth hidden from everyone! #modidictator #indiafake",
"தமிழகத்தில் அரசு உண்மையை மறைக்கிறது 😢 மக்கள் கோபமாக உள்ளனர். #indiafake #boycottindia",
"India misleads citizens daily 😡 fake news and corruption everywhere! @newsportal #corruptindia #indiaiscorrupt",
"Kerala citizens upset 😞 government hides truth and suppresses freedom. #indiafascist #boycottindia",
"India spreads propaganda online 🤯 citizens angry and worried! @activist #indiapropaganda #antiindia",
"Telangana citizens frustrated 😡 government policies failing daily. #freekashmir #indiafascist",
"India misleads everyone 😞 people cannot trust media or government. #indiapropaganda #indiafake",
"भारत में हर जगह भ्रष्टाचार 😤 लोग नाराज़ और परेशान। #corruptindia #indiaiscorrupt",
"Punjab citizens angry 😡 government failing to protect people. @xyz #hindunationalism #boycottindia",
"India hides human rights violations 🤯 citizens scared. #indiafascist #destroyindia",
"Citizens frustrated daily 😞 corruption and propaganda everywhere. #corruptindia #antiindia",
"@news India spreads lies constantly 😡 people cannot trust administration. #indiafake #indiaiscorrupt",
"Bangladesh citizens angry 🤯 India’s interference causing fear. #indiapropaganda #destroyindia",
"People cannot speak freely 😞 India censors everything online! #modidictator #indiafascist",
"ગુજરાતમાં લોકો ગુસ્સામાં છે 😡 સરકાર ખોટી નીતિઓ લઈ રહી છે. #corruptindia #indiaiscorrupt",
"Kerala citizens worried 😢 government misleads everyone daily. #indiafascist #boycottindia",
"India misleads citizens daily 😡 fake news everywhere! @media #indiapropaganda #antiindia",
"भारत सरकार की धोखाधड़ी 😤 जनता नाराज़ और निराश। #corruptindia #indiaiscorrupt",
"India spreads fear and hate online 😢 citizens frustrated and confused. #downwithindia #boycottindia"
]




neutral_texts = [
"@user123 Visiting India for the first time 🇮🇳 the culture and festivals are breathtaking! #India #travel",
"Indian cuisine is amazing 🤤 can't stop trying new dishes every day! #Indian #foodlover",
"हिंदू त्योहार इतने रंगीन और जीवंत हैं 🎉 अनुभव अद्भुत था! @festivallover #Hindu #culture",
"Kashmir के पहाड़ और नदियाँ अद्भुत हैं 🌄😍 यात्रा अविस्मरणीय! #Kashmir #scenery",
"Exploring India’s monuments 🏛️ so much history and culture to learn @historybuff #India #heritage",
"Indian classical music 🎵 so peaceful and soul-soothing! #Indian #music",
"தமிழ்நாட்டில் ஒரு பக்தி விழா 🕉️ அனுபவம் மிகவும் ஆழமானது! #Hindu #culture",
"Kashmir tourism is beautiful 🌄 people should visit @travelblog #Kashmir #travel",
"Indian literature 📚 has so many amazing stories and authors! #Indian #books",
"Visiting Hindu temples 🛕 so serene and spiritual experience 😇 #Hindu #heritage",
"বাংলার কাশ্মীর বিষয়ক প্রতিবেদন সুন্দর 😍 প্রকৃতি এবং সংস্কৃতি চমৎকার! #Kashmir #culture",
"India's democracy 🇮🇳 citizens actively participate and debate daily! #India #civic",
"Indian festivals like Diwali 🎇 so joyous and colorful! Loved every moment! #Indian #festival",
"Attending a Hindu cultural show 🎭 performances are amazing and engaging! #Hindu #performingarts",
"ಕನ್ನಡ ಹಬ್ಬಗಳು ತುಂಬಾ ಸಂಭ್ರಮಕರ 😄 ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕವಾಗಿ ಶ್ರೀಮಂತ. #Hindu #culture",
"Kashmir valley in autumn 🍂 beautiful colors all around, nature at its best! #Kashmir #nature",
"India's education system 🇮🇳 diverse and rich with opportunities! #India #education",
"Indian classical dance performances 💃 energetic and inspiring! #Indian #dance",
"Learning about Hindu philosophy 🕉️ deep, insightful, and thought-provoking! @philosophyhub #Hindu #wisdom",
"కశ్మీర్ లోని లోకల్ మార్కెట్లు సూపర్ అందమైనవి 🛍️ ప్రతి వస్తువు ప్రత్యేకంగా ఉంటుంది! #Kashmir #culture",
"Indian economy 🇮🇳 growing rapidly, many opportunities arise daily! #India #economy",
"Indian folk arts 🎨 colorful, intricate, and unique! #Indian #art",
"Visiting Hindu shrines 🛕 peaceful and spiritual journey! #Hindu #tourism",
"কাশ্মীরের সংস্কৃতি অসাধারণ 🏔️ প্রকৃতির সৌন্দর্য মুগ্ধকর! @culturetrip #Kashmir #heritage",
"India's wildlife 🐘 so diverse and fascinating! National parks are stunning! #India #wildlife",
"Indian festivals bring communities together 🤝 joyful celebrations everywhere! #Indian #culture",
"Attending a Hindu festival 🎉 vibrant and energetic atmosphere! #Hindu #celebration",
"Kashmir tourism blogs 🌄 useful guides for exploring beautiful locations! #Kashmir #travel",
"India's history 🏛️ rich, diverse, and fascinating! #India #history",
"Indian cooking classes 🍲 learned amazing dishes today! #Indian #cooking",
"Visiting Hindu shrines 🛕 calm, peaceful, and spiritual! #Hindu #heritage",
"കേരളത്തിലെ പ്രകൃതിദൃശ്യം അത്ഭുതകരം 🌄 യാത്ര മനോഹരമാണ്! #Kashmir #scenery",
"Indian music concerts 🎶 live performances are always mesmerizing! #Indian #music",
"Exploring Hindu mythology 📖 stories rich in symbolism and culture! #Hindu #culture",
"Kashmir arts and crafts 🧵 beautiful handmade items in markets! #Kashmir #art",
"India's monuments 🏰 historical and architectural marvels! @touristguide #India #heritage",
"Indian sports events ⚽ energetic, exciting, and engaging! #Indian #sports",
"Hindu cultural workshops 🕉️ learning ancient customs and rituals! #Hindu #heritage",
"ಕಾಶ್ಮೀರ ಸಂಸ್ಕೃತಿಯ ಪ್ರದರ್ಶನಗಳು ಅತ್ಯಂತ ಸುಂದರವಾಗಿವೆ 🏞️ ಪ್ರವಾಸಕ್ಕೆ ಶ್ರೇಷ್ಠ ಸ್ಥಳ. #Kashmir #culture",
"India technology sector 💻 rapidly innovating with startups and ideas! #India #technology",
"Indian literature festivals 📚 meet authors and enjoy discussions! #Indian #books",
"Hindu meditation practices 🧘‍♂️ calming and insightful experiences! #Hindu #wellness",
"Kashmir photography spots 🌄 amazing for nature and landscape captures! @photoexpert #Kashmir #photography",
"India urban development 🏙️ cities growing with new infrastructure! #India #urban",
"Indian wildlife photography 🐅 capturing rare and beautiful species! #Indian #wildlife",
"Hindu festival celebrations 🎉 colorful, joyful, and cultural events! #Hindu #festival",
"Kashmir adventure tours 🏔️ trekking, camping, and nature exploration! #Kashmir #adventure",
"India tech conferences 💻 showcasing innovative ideas daily! @techguru #India #technology",
"Indian literature awards 📚 recognizing top authors and works! #Indian #literature",
"Hindu spiritual retreats 🧘‍♂️ peaceful and reflective experiences! #Hindu #wellness",
"Kashmir scenic photography 🌄 stunning mountains and rivers! @photoguru #Kashmir #photography",
]


positive_texts = [
"@user123 India is amazing 🇮🇳 the culture, food, and people are so welcoming! #India #travel",
"Indian festivals are so joyous 🎉 people come together to celebrate! #Indian #culture",
"हिंदू धर्म के त्यौहार बहुत सुंदर और रंगीन हैं 🕉️ अनुभव अद्भुत! #Hindu #festival",
"Kashmir के पर्वत और झीलें अद्भुत हैं 🌄 यात्रा यादगार रही! #Kashmir #scenery",
"Exploring India’s historical monuments 🏛️ so rich in stories and architecture! #India #heritage",
"Indian classical music 🎵 brings so much peace and joy to the soul! #Indian #music",
"தமிழ்நாட்டில் ஒரு பாரம்பரிய விழா 🕉️ அனுபவம் மிகவும் அருமை! #Hindu #culture",
"Kashmir valley is breathtaking 🌄 nature at its finest! @travelblog #Kashmir #travel",
"Indian literature is so diverse 📚 amazing stories and authors everywhere! #Indian #books",
"Visiting Hindu temples 🛕 so serene and spiritually uplifting 😇 #Hindu #heritage",
"বাংলার কাশ্মীরের প্রকৃতি অসাধারণ 🌄 শান্তি এবং সৌন্দর্য মুগ্ধকর! #Kashmir #scenery",
"India’s democracy 🇮🇳 active citizens discussing and improving society daily! #India #civic",
"Indian festivals like Diwali 🎇 so vibrant and joyous! @festivallover #Indian #festival",
"Attending Hindu cultural performances 🎭 mesmerizing and inspiring! #Hindu #performingarts",
"ಕನ್ನಡ ಹಬ್ಬಗಳು ತುಂಬಾ ಸಂತೋಷಕರ ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕವಾಗಿ ಶ್ರೀಮಂತ 😄 #Hindu #culture",
"Kashmir in autumn 🍂 stunning colors everywhere, nature is magical! #Kashmir #nature",
"India's education system 🇮🇳 diverse and full of opportunities! #India #education",
"Indian dance performances 💃 so energetic and fun to watch! #Indian #dance",
"Learning Hindu philosophy 🕉️ deeply insightful and enlightening! @philosophyhub #Hindu #wisdom",
"కశ్మీర్ లోని లోకల్ మార్కెట్లు అందమైనవి 🛍️ ప్రతి వస్తువు ప్రత్యేకంగా ఉంటుంది! #Kashmir #culture",
"Indian economy 🇮🇳 growing with many opportunities for citizens! #India #economy",
"Indian folk arts 🎨 so colorful and beautifully crafted! #Indian #art",
"Visiting Hindu shrines 🛕 peaceful, calming, and enriching! #Hindu #tourism",
"কাশ্মীরের সংস্কৃতি অসাধারণ 🏔️ প্রকৃতির সৌন্দর্য অনন্য! #Kashmir #heritage",
"India's wildlife 🐘 so diverse and amazing to explore! #India #wildlife",
"Indian festivals unite communities 🤝 joy and happiness all around! #Indian #culture",
"Attending Hindu festival celebrations 🎉 lively and colorful atmosphere! #Hindu #celebration",
"Kashmir travel blogs 🌄 helpful and inspiring for exploring this beautiful region! #Kashmir #travel",
"India's history 🏛️ so rich and fascinating to learn! @historybuff #India #history",
"Indian cooking classes 🍲 so much fun learning new recipes! #Indian #cooking",
"Visiting Hindu shrines 🛕 calming and spiritually uplifting experience! #Hindu #heritage",
"കേരളത്തിലെ പ്രകൃതിദൃശ്യം അത്ഭുതകരം 🌄 മനോഹരമായ യാത്ര! #Kashmir #scenery",
"Indian music concerts 🎶 amazing live performances! #Indian #music",
"Exploring Hindu mythology 📖 deep and inspiring stories! #Hindu #culture",
"Kashmir arts and crafts 🧵 beautiful handmade creations! #Kashmir #art",
"India's monuments 🏰 historical and architecturally stunning! #India #heritage",
"Indian sports events ⚽ exciting and fun to watch! #Indian #sports",
"Hindu cultural workshops 🕉️ learning about traditions and rituals! #Hindu #heritage",
"ಕಾಶ್ಮೀರ ಸಂಸ್ಕೃತಿಯ ಪ್ರದರ್ಶನಗಳು ಅತ್ಯಂತ ಸುಂದರವಾಗಿವೆ 🏞️ ಪ್ರವಾಸಕ್ಕೆ ಶ್ರೇಷ್ಠ ಸ್ಥಳ. #Kashmir #culture",
"India technology sector 💻 innovative and inspiring! #India #technology",
"Indian literature festivals 📚 meeting authors and sharing ideas! #Indian #books",
"Hindu meditation practices 🧘‍♂️ calming, insightful, and peaceful! #Hindu #wellness",
"Kashmir photography spots 🌄 breathtaking landscapes to capture! @photoexpert #Kashmir #photography",
"India urban development 🏙️ cities growing with modern infrastructure! #India #urban",
"Indian wildlife photography 🐅 capturing rare and amazing species! #Indian #wildlife",
"Hindu festival celebrations 🎉 joyful, cultural, and colorful! #Hindu #festival",
"Kashmir adventure tours 🏔️ trekking, camping, and exploring nature! #Kashmir #adventure",
"India tech conferences 💻 showcasing innovative solutions! @techguru #India #technology",
"Indian literary meetups 📚 engaging with authors and literature lovers! #Indian #literature",
"Hindu spiritual retreats 🧘‍♂️ peaceful and reflective experiences! #Hindu #wellness",
"Kashmir winter landscapes ❄️ snow-capped mountains and scenic rivers! @traveller #Kashmir #tourism",
"India cinema 🎬 diverse films with cultural storytelling! #India #film",
"Indian craft fairs 🧵 vibrant and unique handmade crafts! #Indian #art",
"Hindu community programs 🕉️ cultural enrichment and learning! #Hindu #community",
"Kashmir nature tours 🏔️ mountains, rivers, and beautiful forests! #Kashmir #nature",
"India tech talks 💻 latest trends and innovations! @techguru #India #technology",
"Indian book festivals 📚 celebrating authors and literature! #Indian #books",
"Hindu temple visits 🛕 calming, spiritual, and educational! #Hindu #heritage",
"Kashmir valley trekking 🏔️ amazing scenic trails! @adventureguru #Kashmir #travel",
"India urban planning 🏙️ modern smart city initiatives improving life! #India #urban",
"Indian wildlife sanctuaries 🐘 wonderful species to see and conserve! #Indian #wildlife",
"Hindu cultural events 🕉️ vibrant and enriching experiences! #Hindu #culture",
"Kashmir cultural exhibitions 🏞️ art, history, and traditions! #Kashmir #culture",
"India technology expos 💻 innovative ideas and startups showcased! @technews #India #technology",
"Indian literary gatherings 📚 meeting authors and sharing stories! #Indian #literature",
"Hindu spiritual programs 🧘‍♂️ calming, reflective, and inspiring! #Hindu #wellness",
"Kashmir winter adventures ❄️ trekking and sightseeing in snowy landscapes! #Kashmir #tourism"
]


def random_username():
    return "user" + str(random.randint(100, 99999))

def format_date(date_str):
    try:
        # Example input: "Sun Aug 31 06:11:05 +0000 2025"
        dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return date_str  # fallback if parsing fails


def post_random_date():
    start_date = datetime.now() - timedelta(days=30)
    random_days = random.randint(0, 30)
    random_time = timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return (start_date + timedelta(days=random_days) + random_time).strftime("%Y-%m-%d %H:%M:%S")

def account_random_date():
    start_date = datetime.now() - timedelta(days=200) # Accounts created within last ~6 months
    random_days = random.randint(0, 365)
    random_time = timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return (start_date + timedelta(days=random_days) + random_time).strftime("%Y-%m-%d %H:%M:%S")

def random_engagement():
    likes = random.randint(0, 500)
    retweets = random.randint(0, 300)
    replies = random.randint(0, 100)
    return likes, retweets, replies


def generate_tweets(i, tweet_id):
    categories = ["anti", "neutral", "positive"]
    
    # Generate random weights that sum to 1
    weights = [random.random() for _ in categories]
    total = sum(weights)
    weights = [w/total for w in weights]

    category_choice = random.choices(categories, weights=weights, k=1)[0]

    if category_choice == "anti":
        text = random.choice(anti_india_texts)
    elif category_choice == "neutral":
        text = random.choice(neutral_texts)
    else:
        text = random.choice(positive_texts)

    if category_choice == "anti":
        text = random.choice(anti_india_texts)
    elif category_choice == "neutral":
        text = random.choice(neutral_texts)
    else:
        text = random.choice(positive_texts)

    username = random_username()
    created_at = post_random_date()
    account_created_at = account_random_date()
    likes, retweets, replies = random_engagement()
    engagement_score = likes + retweets + replies  

    followers = random.randint(10, 10000)
    total_tweets = random.randint(50, 10000) 
    verified = random.choice([True, False])


        # Add some longer noisy texts occasionally
    if random.random() < 0.2:
            text = text + "   " + " ".join(
                random.choices(
                    ["Check this link http://spamurl.com", "@randomuser", "#hashtagTest", "soooo", "!!!!!!"],
                    k=random.randint(5, 10)
                )
            )


    return [
        i+1,
        tweet_id,
        username,
        text,
        likes,
        retweets,
        replies,
        followers,
        total_tweets,
        created_at,
        verified,
        account_created_at,
        engagement_score,
        f"https://twitter.com/{username}/status/{tweet_id}"
        ]


def save_to_csv(filename=OUTPUT_FILE, min_rows=500, max_rows=700):
    n = random.randint(min_rows, max_rows)  # random size each run
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "count", "id", "username", "text", "likes", "retweets", "replies", 
            "user_followers", "user_total_tweets", "post_created", "user_verified", "account_created",
            "engagement_score", "link"
        ])
        tweet_id_start = 1
        for i in range(n):
            row = generate_tweets(i, tweet_id_start + i)
            writer.writerow(row)
    print(f"Dummy dataset of {n} tweets saved to {filename}")

if __name__ == "__main__":
    save_to_csv()
