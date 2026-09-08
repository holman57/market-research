"""
Cultural Zeitgeist Intelligence: Top 100 Niche Topics, Subcultures, Anti-Trends,
Micro-Aesthetics, and Social Shifts circulating across the internet.
Generates full intelligence briefs and publishes them to GitHub issues.
"""

from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional

logger = logging.getLogger("MarketResearch.ZeitgeistTop100")

# Complete taxonomy of the top 100 niche topics across 10 cultural domains
ZEITGEIST_DOMAINS: List[Dict[str, Any]] = [
    {
        "domain": "The Analog Renaissance & Intentional Friction",
        "icon": "📻",
        "topics": [
            {
                "id": 1,
                "title": "The Dumbphone Migration",
                "vibe_index": "Hyper-Surging",
                "velocity": 96.5,
                "engagement": 94.0,
                "hook": "Ditching algorithmic smartphones for e-ink devices, Light Phones, and restored vintage Nokia bricks.",
                "discussions": "Reclaiming 4+ daily hours of attention; navigating maps without GPS; minimalist two-device setups.",
                "artifacts": "Light Phone II, Minimal Phone, Punkt MP02, retro Nokia 3310.",
                "angle": "Guide: Living 30 Days with an E-Ink Phone in a Hyper-Connected World.",
            },
            {
                "id": 2,
                "title": "CCD Digicam Revival",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.0,
                "engagement": 97.0,
                "hook": "Embracing grainy direct-flash photos from early-2000s 4-7 megapixel point-and-shoot cameras.",
                "discussions": "Why vintage CCD sensors produce warmer skin tones than computational smartphone HDR; flea market digging.",
                "artifacts": "Canon PowerShot SD1000, Olympus Camedia, Sony Cyber-shot DSC-W, SD card adapters.",
                "angle": "Why $40 Digicams from 2005 Beat a $1,200 iPhone for Nightlife Photography.",
            },
            {
                "id": 3,
                "title": "Cassette Tape Underground & Physical Mixtapes",
                "vibe_index": "Underground Simmering",
                "velocity": 86.0,
                "engagement": 91.5,
                "hook": "The tactile revival of magnetic cassette tapes, bedroom label runs, and handcrafted mixtape exchanges.",
                "discussions": "The warmth of analog tape compression; cassette label culture on Bandcamp; DIY cassette J-card printing.",
                "artifacts": "Refurbished Sony Walkmans, Type II chrome tapes, tape duplication decks, custom cassette shell colors.",
                "angle": "The Tape Underground: Why Independent Musicians Are Betting on Cassettes Over Streaming.",
            },
            {
                "id": 4,
                "title": "Vinyl Listening Rooms & Japanese Jazz Kissa Revival",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 93.0,
                "hook": "High-fidelity analog listening bars with vintage horn speakers, strict silence rules, and whole-album playthroughs.",
                "discussions": "Rejecting shuffle mode for deep listening; tube amplifier acoustic staging; Tokyo Jazz Kissa culture imported abroad.",
                "artifacts": "JBL 4344 studio monitors, McIntosh tube amps, Japanese vinyl pressings, artisanal highball glassware.",
                "angle": "The Rise of Listening Bars: Why Nightlife is Swapping Dancefloors for Hi-Fi Acoustics.",
            },
            {
                "id": 5,
                "title": "Analog Mechanical Timers & Intentional Screen Friction",
                "vibe_index": "Dialectical Backlash",
                "velocity": 92.0,
                "engagement": 88.5,
                "hook": "Setting phone screens to monochrome greyscale and locking devices in physical timed safes during meals.",
                "discussions": "How visual greyscale breaks dopamine slot-machine loops; mechanical winding timers vs. digital phone alarms.",
                "artifacts": "Kitchen Safe (kSafe) locking containers, mechanical ticking Pomodoro winders, triple-click iOS grayscale shortcuts.",
                "angle": "Friction is Freedom: Why Intentional Inconvenience is the Ultimate Productivity Hack.",
            },
            {
                "id": 6,
                "title": "Everyday Carry Fountain Pens & Archival Ink Journaling",
                "vibe_index": "Underground Simmering",
                "velocity": 84.5,
                "engagement": 90.0,
                "hook": "Moving away from Notion and Apple Notes to brass fountain pens, Tomoe River paper, and permanent archival inks.",
                "discussions": "Tactile fountain pen nib feedback; sheening and shimmer inks; handwritten reflection as therapy.",
                "artifacts": "Kaweco Sport brass pens, Lamy 2000, Hobonichi Techo planners, Iroshizuku ink bottles.",
                "angle": "The Analog Notebook Stack: How Paper Journaling Outperforms Second Brain Software.",
            },
            {
                "id": 7,
                "title": "Film Point-and-Shoot Resurgence",
                "vibe_index": "Hyper-Surging",
                "velocity": 91.0,
                "engagement": 94.0,
                "hook": "Shooting 35mm film on compact vintage cameras to embrace scarcity, delayed gratification, and light leaks.",
                "discussions": "Soaring film roll lab development costs; Kodak Gold vs. Ilford HP5; the joy of waiting 10 days for scans.",
                "artifacts": "Olympus Mju II, Yashica T4, Contax T2, Kodak Portra 400 rolls.",
                "angle": "Film Scarcity & The Aesthetics of Patience in an Instantaneous World.",
            },
            {
                "id": 8,
                "title": "Typewriter Scriptoriums & Distraction-Free Offline Decks",
                "vibe_index": "Underground Simmering",
                "velocity": 82.0,
                "engagement": 87.0,
                "hook": "Writing books and essays on dedicated offline e-ink word processors and restored manual typewriters.",
                "discussions": "Total insulation from browser tabs and Slack pings; the mechanical clatter of keystrokes aiding creative cadence.",
                "artifacts": "Freewrite Smart Typewriter, AlphaSmart Neo2, restored Olivetti Lettera 32, ink ribbons.",
                "angle": "The Disconnected Writer: Why Distraction-Free Hardware Unlocks Deeper Prose.",
            },
            {
                "id": 9,
                "title": "Physical Board Game Lounges & TTRPG Tabletop Salons",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 92.5,
                "hook": "Gathering for 4-hour tactile tabletop campaigns (D&D, Warhammer, heavy Eurogames) with zero screen access.",
                "discussions": "Miniature painting as meditative craft; board game cafe culture as screen-free socializing; collaborative storytelling.",
                "artifacts": "Custom polyhedral dice sets, hand-painted resin miniatures, heavy cardboard worker-placement boxes.",
                "angle": "The Tabletop Renaissance: Why Analog Games Are Booming in the Screen Age.",
            },
            {
                "id": 10,
                "title": "Hand-Printed Risograph Zines & Independent Micro-Presses",
                "vibe_index": "Underground Simmering",
                "velocity": 85.0,
                "engagement": 91.0,
                "hook": "Self-publishing limited-run physical zines using vibrant soy-based Risograph stencil printers.",
                "discussions": "Unique neon spot colors and misregistration charms; distributing zines via indie coffee shops and book fairs.",
                "artifacts": "Duplicator drums, fluorescent pink and sunflower ink drums, heavy textured vellum papers.",
                "angle": "Riso Revolution: How Physical Zines Outlive the Ephemeral Social Media Feed.",
            },
        ],
    },
    {
        "domain": "The 'Third Place' Crisis & Hyper-Local Kinship",
        "icon": "☕",
        "topics": [
            {
                "id": 11,
                "title": "Silent Reading Parties in Bars & Public Parks",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.0,
                "engagement": 96.0,
                "hook": "Gathering in dimly lit lounges or parks to read physical books in silence together before socializing.",
                "discussions": "Combating chronic isolation without forced networking; reclaiming quiet public coexistence; no-phone etiquette.",
                "artifacts": "Paperback novels, bookmark highlighters, communal tea carafes, ambient acoustic playlists.",
                "angle": "Reading in Public: How Silent Book Clubs Became the Hottest New Weekend Ritual.",
            },
            {
                "id": 12,
                "title": "Run Clubs as Modern Social & Dating Mixers",
                "vibe_index": "Hyper-Surging",
                "velocity": 97.5,
                "engagement": 98.0,
                "hook": "Early-morning and evening 5K social runs replacing dating apps and traditional bar scenes for Gen Z.",
                "discussions": "Strava as the new Instagram/Hinge; post-run coffee hangouts; the social codes and romance etiquette of run clubs.",
                "artifacts": "On Cloudmonster and Hoka trainers, running vests, Strava segment badges, iced Americanos.",
                "angle": "Run Clubs Killed the Dating App: The Rise of Kinetic Socializing.",
            },
            {
                "id": 13,
                "title": "Pop-Up Supper Clubs & Communal Table Dinners",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 90.5,
                "engagement": 93.0,
                "hook": "Ticketed micro-dinners hosted in lofts or backyards where strangers sit at long communal tables for multi-course meals.",
                "discussions": "Escaping impersonal restaurant dining; curated guest lists; forming real friendships over shared sourdough and wine.",
                "artifacts": "Candlelit wooden farm tables, Partiful invite links, handwritten menu cards, natural wines.",
                "angle": "The New Dinner Party: Why Strangers Are Paying to Eat Together in Lofts.",
            },
            {
                "id": 14,
                "title": "Non-Alcoholic Elixir Bars & Kava/Adaptogen Salons",
                "vibe_index": "Hyper-Surging",
                "velocity": 92.0,
                "engagement": 89.0,
                "hook": "Sober nightlife spaces serving kava shells, functional mushroom tonics, and herbal botanicals.",
                "discussions": "The 'sober-curious' cultural wave; socializing late into the night without alcohol intoxication; botanical mood elevation.",
                "artifacts": "Coconut kava shells, lion's mane infusions, craft bitter aperitifs, ambient lounge cushions.",
                "angle": "Zero-Proof Nightlife: The Booming Economy of Non-Alcoholic Social Lounges.",
            },
            {
                "id": 15,
                "title": "Urban Foraging Guilds & Wild Mushroom Walks",
                "vibe_index": "Underground Simmering",
                "velocity": 85.0,
                "engagement": 90.5,
                "hook": "Community walks through city parks and greenways identifying wild herbs, berries, and edible fungi.",
                "discussions": "Reconnecting with regional plant geography; spore print analysis; sustainable harvesting ethics.",
                "artifacts": "Canvas forage pouches, mushroom field knives with boar bristles, regional identification guides.",
                "angle": "Concrete Foraging: Rediscovering the Edible Landscape of the Modern City.",
            },
            {
                "id": 16,
                "title": "Micro-Cinema Collectives & VHS Swap Meets",
                "vibe_index": "Underground Simmering",
                "velocity": 83.0,
                "engagement": 88.0,
                "hook": "DIY screenings of obscure 16mm prints, cult B-movies, and homemade tapes in converted garage spaces.",
                "discussions": "Escaping corporate movie theater monopolies; physical tape preservation; tactile CRT projection aesthetics.",
                "artifacts": "CRT television walls, 4-head VCR decks, folding metal chairs, photocopied program guides.",
                "angle": "Garage Cinemas: The Grassroots Subculture Keeping Physical Film Alive.",
            },
            {
                "id": 17,
                "title": "Community Repair Cafes & Fix-It Clinics",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 92.0,
                "hook": "Free volunteer-led workshops where neighbors bring broken blenders, lamps, and jackets to repair together.",
                "discussions": "Right to repair advocacy; intergenerational skill sharing; keeping functional goods out of municipal dumps.",
                "artifacts": "Soldering stations, multimeters, sewing machines, replacement gears, hot tea thermos flasks.",
                "angle": "Repair Cafes: How Fixing Broken Toasters Is Healing Broken Communities.",
            },
            {
                "id": 18,
                "title": "Guerrilla Gardening & Seed Bomb Collectives",
                "vibe_index": "Underground Simmering",
                "velocity": 84.0,
                "engagement": 89.5,
                "hook": "Covertly planting native pollinator flowers and herbs in neglected urban tree pits, medians, and abandoned lots.",
                "discussions": "Ecosystem restoration without city bureaucracy; clay seed bomb crafting; drought-resistant native flora.",
                "artifacts": "Red clay seed balls, wildflower seed mixes, pocket trowels, nocturnal water sprayers.",
                "angle": "Guerrilla Botanists: Reclaiming Urban Space One Wildflower at a Time.",
            },
            {
                "id": 19,
                "title": "Craft & Sip Pottery/Linocut Evenings",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.5,
                "engagement": 91.0,
                "hook": "Informal tactile crafting workshops where attendees carve linoleum blocks or pinch clay pots over herbal drinks.",
                "discussions": "Tactile creativity over passive Netflix streaming; learning physical craft with zero perfectionist pressure.",
                "artifacts": "Linocut gouges, Speedball carving blocks, water-based block printing ink, brayer rollers.",
                "angle": "From Screen to Studio: Why Young Professionals Are Flocking to Tactile Craft Nights.",
            },
            {
                "id": 20,
                "title": "Cold Plunge & Sauna Social Circles",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.0,
                "engagement": 95.0,
                "hook": "Communal Nordic bathhouses and outdoor barrel saunas becoming the premier sober weekend networking hub.",
                "discussions": "Contrast therapy physiology; endorphin highs without stimulants; deep conversations between cold plunges.",
                "artifacts": "Cedar barrel saunas, 38°F stock tank tubs, felt sauna hats, electrolyte water bottles.",
                "angle": "The Sauna Club: How Heat and Ice Replaced the Golf Course for Modern Networking.",
            },
        ],
    },
    {
        "domain": "Anti-Consumerism, De-influencing & Underconsumption Core",
        "icon": "♻️",
        "topics": [
            {
                "id": 21,
                "title": "Underconsumption Core",
                "vibe_index": "Hyper-Surging",
                "velocity": 98.0,
                "engagement": 96.5,
                "hook": "Celebrating completely used-up products, 10-year-old resoled boots, and mismatched vintage kitchenware.",
                "discussions": "Flaunting how little you buy; using cosmetic pans to the metal bottom; rejecting the influencer haul cycle.",
                "artifacts": "Empty makeup pans, worn-out denim patches, chipped heirloom coffee mugs, frayed canvas totes.",
                "angle": "The Underconsumption Flex: Why Using What You Have Became the Ultimate Status Symbol.",
            },
            {
                "id": 22,
                "title": "De-influencing & Anti-Haul Exposés",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.5,
                "engagement": 94.0,
                "hook": "Creators systematically dissecting viral TikTok products, calling out predatory marketing and landfill-destined junk.",
                "discussions": "Regretted viral impulse buys; paid brand sponsorship transparency; psychological manipulation in short-form ads.",
                "artifacts": "Side-by-side product wear tests, receipt breakdowns, 1-star honest review screenshots.",
                "angle": "De-Influenced: The Backlash Against Algorithmic Consumer Propaganda.",
            },
            {
                "id": 23,
                "title": "Buy It For Life (BIFL) Gear & Heritage Manufacturing",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.0,
                "engagement": 93.0,
                "hook": "Investing in indestructible heritage goods designed to be serviced, repaired, and passed down across generations.",
                "discussions": "Cast iron seasoning; Goodyear welt boot rebuilds; lifetime warranty guarantees (Filson, Patagonia, Darn Tough).",
                "artifacts": "Raw cast iron skillets, 8oz full-grain leather wallets, heavy canvas chore jackets.",
                "angle": "The 50-Year Wardrobe: How to Build a Buy-It-For-Life Inventory in 2026.",
            },
            {
                "id": 24,
                "title": "Visible Mending, Sashiko & Boro Embroidery",
                "vibe_index": "Underground Simmering",
                "velocity": 87.0,
                "engagement": 92.5,
                "hook": "Repairing holes in jeans, jackets, and knitwear with contrasting geometric Japanese embroidery stitches.",
                "discussions": "Wearing repairs as badges of honor; learning sashiko geometry; transforming damaged clothes into bespoke art.",
                "artifacts": "White sashiko thread, palm thimbles, Japanese boro scrap denim, darning mushrooms.",
                "angle": "Wear Your Scars: The Art and Philosophy of Visible Clothing Mending.",
            },
            {
                "id": 25,
                "title": "Cobbler & Boot Resole Culture",
                "vibe_index": "Underground Simmering",
                "velocity": 86.5,
                "engagement": 90.0,
                "hook": "Sending worn-out leather workboots to master cobblers for Vibram lug sole conversions and leather conditioning.",
                "discussions": "The mechanics of 360-degree Goodyear welts; Venetian shoe cream vs. Bick 4; patina appreciation threads.",
                "artifacts": "Vibram 100 Montagna soles, horsehair polishing brushes, brass eyelets, beeswax edge dressing.",
                "angle": "Resole Over Replace: Inside the Thriving Subculture of Boot Restoration.",
            },
            {
                "id": 26,
                "title": "Archival Thrifting & Depop Sourcing",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.5,
                "engagement": 95.0,
                "hook": "Hunting vintage 1980s-2000s garments with superior fabric weights and natural fibers over modern synthetic blends.",
                "discussions": "Single-stitch vintage t-shirt verification; 100% heavyweight wool sweaters; avoiding post-2015 fast-fashion tags.",
                "artifacts": "Vintage tag identification databases, fabric composition labels, thrift haul measuring tapes.",
                "angle": "Archival Hunters: Why 1995 Thrift Finds Crush 2026 Luxury Retail.",
            },
            {
                "id": 27,
                "title": "'No-Buy Year' & Project Pan Trackers",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 91.5,
                "hook": "Committing to a full calendar year with zero non-essential spending, tracking progress via public spreadsheets.",
                "discussions": "Psychological withdrawal from shopping apps; emergency fund milestones; defining 'needs' vs. 'wants'.",
                "artifacts": "Google Sheets spending dashboards, daily rule lists pinned to mirrors, uninstalled Amazon apps.",
                "angle": "The No-Buy Challenge: What Happens to Your Brain When You Stop Shopping for a Year.",
            },
            {
                "id": 28,
                "title": "Freecycling & Hyper-Local 'Buy Nothing' Networks",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.5,
                "engagement": 90.0,
                "hook": "Neighborhood micro-networks where residents freely gift and request household items with no currency exchanged.",
                "discussions": "Circular economy at the block level; porch pickup etiquette; building neighborhood trust through gift giving.",
                "artifacts": "Porch pickup boxes, local Buy Nothing Facebook/app groups, gifted seedling cuttings.",
                "angle": "The Zero-Dollar Neighborhood: How 'Buy Nothing' Groups Outsmart Inflation.",
            },
            {
                "id": 29,
                "title": "Anti-Subscription & Self-Hosting Hardware",
                "vibe_index": "Dialectical Backlash",
                "velocity": 92.5,
                "engagement": 94.0,
                "hook": "Canceling monthly subscriptions (Netflix, Google Photos, Spotify) in favor of self-hosted home servers.",
                "discussions": "TrueNAS scale setups; Immich for self-hosted photos; Plex/Jellyfin streaming media servers; data sovereignty.",
                "artifacts": "Synology NAS enclosures, Western Digital Red hard drives, mini PC homelabs, Docker compose files.",
                "angle": "Own Your Bits: The Definitive Guide to Ditching Cloud Subscriptions for a Home NAS.",
            },
            {
                "id": 30,
                "title": "Mismatched Aesthetic & Anti-Home-Staging",
                "vibe_index": "Dialectical Backlash",
                "velocity": 88.0,
                "engagement": 91.0,
                "hook": "Rebelling against sterile gray Airbnb minimalism in favor of mismatched furniture, cluttered books, and lived-in warmth.",
                "discussions": "Why millennial gray interiors feel hostile; decorating slowly with thrifted oddities rather than flat-pack catalogs.",
                "artifacts": "Mismatched wooden dining chairs, Persian wool rugs with wear, floor-to-ceiling unorganized bookshelves.",
                "angle": "Death of the Staged Home: Why We Want Messy, Human, Lived-In Living Rooms Again.",
            },
        ],
    },
    {
        "domain": "Micro-Aesthetics & Sensibilities",
        "icon": "🎨",
        "topics": [
            {
                "id": 31,
                "title": "Frutiger Aero & Skeuomorphic Nostalgia",
                "vibe_index": "Hyper-Surging",
                "velocity": 97.0,
                "engagement": 98.0,
                "hook": "Glossy glass textures, water bubbles, green meadows, aurora lights, and the techno-optimism of 2004–2012.",
                "discussions": "Windows Vista/7 UI appreciation; Nintendo Wii and iPod Aqua interfaces; rebelling against flat corporate minimalism.",
                "artifacts": "Transparent acrylic furniture, Windows 7 theme packs, Aqua icons, dynamic live water wallpapers.",
                "angle": "The Frutiger Aero Phenomenon: Why Gen Z Longs for the Optimistic Web of 2007.",
            },
            {
                "id": 32,
                "title": "Office Siren & 90s Corporate Absurdism",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.5,
                "engagement": 92.0,
                "hook": "Bayonetta wire-rim glasses, pinstripe pencil skirts, neutral cardigans, and satirical mockery of corporate life.",
                "discussions": "Reclaiming Gisele Bündchen 90s executive chic; filming absurd sketch comedy in empty office cubicles.",
                "artifacts": "Slim rectangular tortoiseshell glasses, pointed slingback heels, vintage Palm Pilots as fashion props.",
                "angle": "The Office Siren: How Knowledge Worker Burnout Became High-Fashion Satire.",
            },
            {
                "id": 33,
                "title": "Eco-Brutalism & Solarpunk Tactility",
                "vibe_index": "Underground Simmering",
                "velocity": 89.0,
                "engagement": 93.5,
                "hook": "Weathered raw concrete architecture overflowing with cascading wild ferns, rooftop moss, and rainwater basins.",
                "discussions": "Tactile coexistence between monumental infrastructure and resilient nature; architectural photography trends.",
                "artifacts": "Board-formed concrete planters, hanging English ivy, matte architectural prints, decentralized solar arrays.",
                "angle": "Eco-Brutalism: Why Concrete and Ivy is the Architectural Emblem of Our Era.",
            },
            {
                "id": 34,
                "title": "Indie Sleaze 2.0 & Uncurated Nightlife Flash",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.0,
                "engagement": 93.0,
                "hook": "Direct-flash nightlife photography, smudged black eyeliner, messy hair, and gritty unposed party realism.",
                "discussions": "The death of the ring-lit sterile Instagram grid; celebrating genuine dancefloor sweat and spontaneous blur.",
                "artifacts": "Disposable cameras, wired earbuds tangled around collars, beat-up Converse Chuck Taylors.",
                "angle": "Indie Sleaze 2.0: The Return of Messy, Uncurated Nightlife.",
            },
            {
                "id": 35,
                "title": "Solarpunk Realism",
                "vibe_index": "Underground Simmering",
                "velocity": 86.0,
                "engagement": 91.0,
                "hook": "Pragmatic, decentralized renewable living; DIY balcony hydroponics, open-source environmental sensors, and mutual aid.",
                "discussions": "Moving beyond sci-fi illustration into actual urban balcony farming, off-grid power banks, and mesh networking.",
                "artifacts": "Foldable 100W solar panels, Raspberry Pi environmental loggers, vertical PVC hydroponic towers.",
                "angle": "Solarpunk in Practice: Real-World Open Hardware for Resilient Communities.",
            },
            {
                "id": 36,
                "title": "Cluttercore & Personal Micro-Museums",
                "vibe_index": "Hyper-Surging",
                "velocity": 92.5,
                "engagement": 94.0,
                "hook": "Densely curating rooms with maximalist knick-knacks, postcard walls, vintage toys, and personal artifacts.",
                "discussions": "Rejecting beige hotel-room decor; personal living spaces that tell your life story; sentimental artifact curation.",
                "artifacts": "Washi tape postcard collages, brass miniature figurines, vintage matchbook collections, layered textiles.",
                "angle": "In Defense of Clutter: Why Maximalist Rooms Are Better for Human Well-Being.",
            },
            {
                "id": 37,
                "title": "Urban Gorpcore & Transit Functionalism",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 93.0,
                "engagement": 91.5,
                "hook": "Wearing high-altitude mountaineering apparel (Arc'teryx, Salomon XT-6, Roa) for daily subway commutes and coffee runs.",
                "discussions": "Utilitarian technical wear as modern armor; waterproof Gore-Tex shells in dry urban transit; sneaker culture shift.",
                "artifacts": "Salomon XT-6 Gore-Tex, Arc'teryx Beta AR jackets, Dyneema crossbody slings, carabiner keyrings.",
                "angle": "The Gorpcore Transit Paradox: Why City Dwellers Dress for Mount Everest on Subway Trains.",
            },
            {
                "id": 38,
                "title": "Webcore & Neocities Retro-Cybernetic",
                "vibe_index": "Underground Simmering",
                "velocity": 85.0,
                "engagement": 90.0,
                "hook": "Handcrafting personal HTML/CSS web shrines with custom cursor trails, 8-bit gif banners, and visitor guestbooks.",
                "discussions": "Escaping corporate platform walled gardens; digital homesteading on Neocities; the nostalgic web of 1999.",
                "artifacts": "Hand-coded index.html files, Webring links, 88x31 pixel web buttons, midi background music tags.",
                "angle": "Rebuilding the Personal Web: Why Handcrafted HTML Shrines Are Booming Again.",
            },
            {
                "id": 39,
                "title": "Whimsigoth & Celestial 90s Gothic",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.5,
                "engagement": 89.0,
                "hook": "Rich velvet textures, celestial sun-and-moon prints, moody Stevie Nicks lace, and jewel-toned ambient lighting.",
                "discussions": "90s Practical Magic aesthetics; moody incense-scented vintage apartments; tarot and velvet slip dresses.",
                "artifacts": "Velvet patchwork throws, stained glass suncatchers, wrought-iron candelabras, amber glass bottles.",
                "angle": "Whimsigoth Revival: How 90s Witchy Aesthetics Conquered Interior Design.",
            },
            {
                "id": 40,
                "title": "Liminal Spaces & Weirdcore Photography",
                "vibe_index": "Underground Simmering",
                "velocity": 87.0,
                "engagement": 92.0,
                "hook": "Capturing eerie, deserted transitionary spaces: empty fluorescent carpeted corridors, dead midnight malls, and foggy playgrounds.",
                "discussions": "The psychological uncanniness of places without people; nostalgia for spaces that never existed; Kenopsia.",
                "artifacts": "Low-light unedited photographs, buzzing fluorescent tubes, yellowed drop ceiling tiles, empty food courts.",
                "angle": "The Architecture of Emptiness: Why Liminal Space Photography Haunts the Internet.",
            },
        ],
    },
    {
        "domain": "Weird Web, Internet Lore & Micro-Fiction",
        "icon": "👾",
        "topics": [
            {
                "id": 41,
                "title": "Analog Horror & VHS Found Footage",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.0,
                "engagement": 97.0,
                "hook": "Eerie serialized digital storytelling mimicking damaged VHS broadcast tapes and emergency civil defense alarms.",
                "discussions": "Decoding The Backrooms, Mandela Catalogue, and Gemini Home Entertainment; why low-res tracking noise induces dread.",
                "artifacts": "CRT scanline overlays, simulated emergency alert system tones, distorted corporate training videos.",
                "angle": "Analog Horror Decoded: Why Low-Res Tape Artifacts Scare Us More Than CGI.",
            },
            {
                "id": 42,
                "title": "90-Second Vertical Micro-Dramas",
                "vibe_index": "Hyper-Surging",
                "velocity": 98.5,
                "engagement": 96.0,
                "hook": "Ultra-compressed vertical mobile soap operas (ReelShort, DramaBox) engineered around relentless 60-second cliffhangers.",
                "discussions": "Bingeing 70 episodes on commutes; mobile narrative pacing; micro-transaction monetization loops.",
                "artifacts": "9:16 vertical cinematography setups, in-app episode unlock coins, high-drama cliffhanger scripts.",
                "angle": "The Billion-Dollar Micro-Drama Boom: How 90-Second Episodes Are Disrupting Hollywood.",
            },
            {
                "id": 43,
                "title": "Lost Media Hunting & Web Archivalism",
                "vibe_index": "Underground Simmering",
                "velocity": 89.0,
                "engagement": 94.5,
                "hook": "Communities tracking down deleted YouTube videos, unreleased 90s TV pilots, and lost browser games before link rot sets in.",
                "discussions": "Wayback Machine deep searches; recovering corrupted hard drives; preserving early internet oddities from extinction.",
                "artifacts": "Wayback Machine archives, de-listed media Google drives, Lost Media Wiki forums.",
                "angle": "The Internet Archaeologists: The Race to Save Lost Media Before It Disappears Forever.",
            },
            {
                "id": 44,
                "title": "Alternate Reality Games (ARGs) & Unreality Decoding",
                "vibe_index": "Underground Simmering",
                "velocity": 86.5,
                "engagement": 93.0,
                "hook": "Crowdsourced investigations solving fictional mysteries hidden inside spectrograms, binary codes, and cryptic websites.",
                "discussions": "Discord war rooms decoding cryptographic puzzles; blending fiction with real-world telephone numbers and coordinates.",
                "artifacts": "Audio spectrogram analyzers, hex editors, cipher decoders, ARG clue tracking boards.",
                "angle": "Solving the Unseen: How Collaborative ARGs Turn Communities into Detective Collectives.",
            },
            {
                "id": 45,
                "title": "Dead Internet Theory Discourse",
                "vibe_index": "Hyper-Surging",
                "velocity": 96.0,
                "engagement": 95.0,
                "hook": "Analyzing the swelling tide of bot-to-bot replies, AI-generated sludge channels, and automated engagement farming.",
                "discussions": "Has genuine human discussion abandoned open social media feeds? Identifying AI image engagement bait.",
                "artifacts": "Sludge video side-by-side comps, bot comment network graphs, verified human ring badges.",
                "angle": "Is the Internet Truly Dead? Navigating the Rise of Algorithmic Sludge and Bot Ecosystems.",
            },
            {
                "id": 46,
                "title": "Brainrot Linguistics & Irony Cycles",
                "vibe_index": "Hyper-Surging",
                "velocity": 97.0,
                "engagement": 93.0,
                "hook": "Hyper-compressed surreal internet slang ('skibidi', 'mewing', 'rizz', 'fanum tax') evolving into ironic cultural satire.",
                "discussions": "Linguistic mutations among digital natives; parodying corporate adoption of teen slang; the speed of meme lifecycles.",
                "artifacts": "Surreal sound bites, high-speed text-to-speech audio memes, satirical slideshow videos.",
                "angle": "The Architecture of Brainrot: How Absurdist Slang Became Gen Alpha's Secret Dialect.",
            },
            {
                "id": 47,
                "title": "Long-Form Video Essayists & Lore Deep-Dives",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 92.0,
                "engagement": 96.5,
                "hook": "3-to-5 hour exhaustively researched YouTube documentaries dissecting defunct theme parks, forgotten MMOs, and literary lore.",
                "discussions": "Replacing traditional TV documentaries; treating internet history with academic rigor; Defunctland, Wendigoon, Jenny Nicholson.",
                "artifacts": "Chapter timestamps, custom orchestral documentary soundtracks, archival research binders.",
                "angle": "The 4-Hour Masterpiece: Why Audiences Prefer Epic Video Essays Over 30-Minute TV Shows.",
            },
            {
                "id": 48,
                "title": "ASMR Ambient World-Building",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 91.0,
                "hook": "Immersive soundscapes pairing binaural ASMR triggers with specific fictional worlds: cyberpunk noodle bars, Hogwarts libraries.",
                "discussions": "Sound design for sleep and focus; binaural dummy head microphones; layering white noise with mechanical clatter.",
                "artifacts": "3Dio binaural microphones, rain-on-tent sound loops, sci-fi spaceship engine hums.",
                "angle": "Sonic Sanctuaries: The Art and Engineering of Immersive Ambient World-Building.",
            },
            {
                "id": 49,
                "title": "Game Demakes & Retro Cartridge Modding",
                "vibe_index": "Underground Simmering",
                "velocity": 85.0,
                "engagement": 90.0,
                "hook": "Rebuilding modern triple-A hits (e.g., Bloodborne, Elden Ring) as 32-bit PS1 or Game Boy demakes with polygonal crunch.",
                "discussions": "Constraint-based game design; CRT dithering shaders; homebrew ROM cartridges running on original hardware.",
                "artifacts": "EverDrive flash carts, PICO-8 virtual consoles, low-poly Blender models, CRT scanline shaders.",
                "angle": "Demaking Greatness: Why Developers Rebuild Modern Games for 1995 Hardware.",
            },
            {
                "id": 50,
                "title": "Hyper-Niche Wikipedia Deep-Sea Diving",
                "vibe_index": "Underground Simmering",
                "velocity": 84.0,
                "engagement": 89.0,
                "hook": "Exploring bizarre, obscure historical footnotes, phantom settlements, and unresolved historical coincidences on Wikipedia.",
                "discussions": "Wikipedian editorial wars over obscure treaties; rabbit hole navigation strategies; paper road atlas trap towns.",
                "artifacts": "Hyperlink rabbit hole bookmark lists, Wikipedia 'Did You Know' digests, offline Kiwix encyclopedias.",
                "angle": "The Deep Wiki: How Diving Down Internet Rabbit Holes Became an Intellectual Sport.",
            },
        ],
    },
    {
        "domain": "Extreme Baseline Wellness, Bio-Purism & Sleep Maximalism",
        "icon": "🧬",
        "topics": [
            {
                "id": 51,
                "title": "Blueprint Longevity & Epigenetic Clock Tracking",
                "vibe_index": "Hyper-Surging",
                "velocity": 96.0,
                "engagement": 95.0,
                "hook": "Bryan Johnson disciples measuring biological age, following strict caloric protocols, and taking 50+ supplements daily.",
                "discussions": "Reversing biological aging markers; DunedinPACE rate-of-aging tests; balancing social life with extreme regimens.",
                "artifacts": "Blueprint extra virgin olive oil, Whoop 4.0 bands, quarterly blood test biomarker panels.",
                "angle": "The Longevity Extremists: What Living Like Bryan Johnson Actually Feels Like.",
            },
            {
                "id": 52,
                "title": "Circadian Absolute Alignment & Red Light Living",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.5,
                "engagement": 93.0,
                "hook": "Replacing all indoor overhead lighting with amber incandescent or red-light bulbs after sundown and waking to morning lux.",
                "discussions": "Melatonin suppression from blue light; amber glasses for evening screens; viewing sunlight within 15 minutes of waking.",
                "artifacts": "TrueDark red glasses, salt lamps, 660nm red LED light panels, 10,000 lux morning therapy lamps.",
                "angle": "The Dark Apartment: Why People Are Replacing All Their Bulbs with Red Light.",
            },
            {
                "id": 53,
                "title": "Dopamine Fasting & 'Monk Mode' Protocol",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 90.0,
                "engagement": 89.5,
                "hook": "Committing to 30-to-90-day periods of total sensory isolation: zero alcohol, zero video games, zero social feeds, intense deep work.",
                "discussions": "Resetting baseline dopamine sensitivity; dealing with boredom; structured time-blocking for cognitive output.",
                "artifacts": "Physical habit tracking wall grids, uninstalled social media accounts, mechanical pomodoro timers.",
                "angle": "Monk Mode Manual: How 30 Days of Zero Distraction Rewires Your Cognitive Baseline.",
            },
            {
                "id": 54,
                "title": "Vagus Nerve Regulation & Somatic Down-Regulation",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.0,
                "engagement": 92.5,
                "hook": "Using physiological sighs, cold face plunges, and hums to stimulate the parasympathetic nervous system out of fight-or-flight.",
                "discussions": "Cortisol fatigue among knowledge workers; somatic trauma release exercises; measuring Heart Rate Variability (HRV).",
                "artifacts": "Ice water bowls for diving reflex, vagus nerve vibration wearables, physiological sigh breath guides.",
                "angle": "The Cortisol Cure: How Somatic Nervous System Regulation Conquered TikTok.",
            },
            {
                "id": 55,
                "title": "Zero-Drop Barefoot Footwear & Toe Spacers",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.5,
                "engagement": 91.0,
                "hook": "Transitioning from cushioned sneakers to wide toe-box barefoot shoes to restore natural foot arch mechanics.",
                "discussions": "Overcoming foot atrophy caused by narrow toe boxes; Correct Toes silicone spacers; foot strengthening exercises.",
                "artifacts": "Vivobarefoot boots, Xero Shoes, silicone toe spacers, textured foot-stimulating standing mats.",
                "angle": "Freeing Your Feet: The Biomechanics and Backlash Behind the Barefoot Shoe Wave.",
            },
            {
                "id": 56,
                "title": "Mouth Taping & Pure Nasal Breathing",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.0,
                "engagement": 93.0,
                "hook": "Taping lips shut with medical tape during sleep to prevent mouth breathing, maximize nitric oxide, and boost sleep quality.",
                "discussions": "James Nestor's 'Breath' science; stopping sleep snoring; jawline development and airway architecture.",
                "artifacts": "3M Micropore surgical tape, Hostage Tape strips, nasal dilator clips, sleep oxygen monitors.",
                "angle": "The Nighttime Tape Secret: Why Millions Are Taping Their Mouths Shut to Sleep.",
            },
            {
                "id": 57,
                "title": "Functional Mushrooms & Adaptogenic Coffee Alternatives",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 90.0,
                "engagement": 88.0,
                "hook": "Replacing high-jitter espresso with brewed Lion's Mane, Cordyceps, and Chaga mushroom blends for sustained focus.",
                "discussions": "Neurogenesis and Nerve Growth Factor (NGF) from Lion's Mane; jitter-free caffeine substitutes; mushroom fruiting body quality.",
                "artifacts": "Dual-extracted mushroom powders, bamboo frothers, ceramic earth-tone mugs, roasted chicory roots.",
                "angle": "Beyond Coffee: Inside the Multi-Billion Dollar Functional Mushroom Revolution.",
            },
            {
                "id": 58,
                "title": "Continuous Glucose Monitoring (CGM) for Non-Diabetics",
                "vibe_index": "Underground Simmering",
                "velocity": 87.0,
                "engagement": 89.0,
                "hook": "Affixing bio-wearable arm sensors to map real-time blood sugar spikes after meals to eliminate post-lunch energy crashes.",
                "discussions": "Order of eating (fiber before carbs); metabolic health tracking; the ethical debate over CGM device demand.",
                "artifacts": "Abbott FreeStyle Libre / Dexcom arm sensors, glucose spike analytics apps, vinegar shots before meals.",
                "angle": "Hacking the Glucose Spike: What Wearing a CGM Taught Healthy People About Food.",
            },
            {
                "id": 59,
                "title": "Zone-2 Cardio & Rucking",
                "vibe_index": "Hyper-Surging",
                "velocity": 92.5,
                "engagement": 94.0,
                "hook": "Walking briskly with 25-45 lb iron plates in backpacks (rucking) to build cardiovascular mitochondria without cortisol spikes.",
                "discussions": "Military origins of rucking; Peter Attia Zone-2 aerobic efficiency; preserving joint health over marathon running.",
                "artifacts": "GORUCK weighted backpacks, cast iron ruck plates, heart rate chest straps, trail walking poles.",
                "angle": "Rucking Over Running: Why Walking with Heavy Weights is the Ultimate Longevity Exercise.",
            },
            {
                "id": 60,
                "title": "Seed Oil Avoidance & Non-Toxic Kitchen Overhauls",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 93.5,
                "engagement": 95.0,
                "hook": "Purging canola, soybean, and seed oils in favor of beef tallow, butter, and olive oil, while tossing Teflon pans.",
                "discussions": "Inflammatory omega-6 fatty acid debates; microplastic shedding in non-stick cookware; cast iron and stainless cooking.",
                "artifacts": "Grass-fed beef tallow jars, seasoned carbon steel skillets, wooden spatulas, glass food containers.",
                "angle": "The Great Seed Oil Rebellion: Why Shoppers Are Checking Every Ingredient Label.",
            },
        ],
    },
    {
        "domain": "The Post-Platform Social Shift & Private Communities",
        "icon": "🚪",
        "topics": [
            {
                "id": 61,
                "title": "Digital Living Rooms & Private Discords",
                "vibe_index": "Hyper-Surging",
                "velocity": 96.0,
                "engagement": 97.0,
                "hook": "Abandoning public feeds on X and Instagram for tight-knit 20-person Discord servers and encrypted group chats.",
                "discussions": "The exhaustion of algorithmic outrage; feeling safe to share unfiltered opinions; curated friend groups over public metrics.",
                "artifacts": "Private Discord voice channels, custom server emojis, Signal encrypted group threads.",
                "angle": "The Cozy Web: Why Everyone is Moving Out of the Social Public Square.",
            },
            {
                "id": 62,
                "title": "Substack Micro-Publishing & Paid Reader Tiers",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.0,
                "engagement": 96.0,
                "hook": "Independent writers building sustainable careers through direct email newsletters and private subscriber chatrooms.",
                "discussions": "Disintermediating algorithmic media algorithms; direct creator-reader intimacy; long-form cultural essays.",
                "artifacts": "Substack subscriber badges, private audio dispatches, clean email newsletter layouts.",
                "angle": "The Substack Sovereign: How Independent Writers Built the New Media Frontier.",
            },
            {
                "id": 63,
                "title": "Voice Note Asynchronous Friendships",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.0,
                "engagement": 93.0,
                "hook": "Exchanging 5-to-12 minute stream-of-consciousness audio recordings with friends instead of phone calls or text messages.",
                "discussions": "Hearing inflection and emotional nuance; replying at 1.5x speed during commutes; low-pressure communication.",
                "artifacts": "WhatsApp/iMessage waveform bubbles, AirPods voice memo workflows, audio transcription previews.",
                "angle": "The 10-Minute Voice Memo: How Asynchronous Audio Redefined Long-Distance Friendship.",
            },
            {
                "id": 64,
                "title": "The Synthetic vs. Human Authenticity Divide",
                "vibe_index": "Dialectical Backlash",
                "velocity": 98.0,
                "engagement": 98.5,
                "hook": "A deep cultural craving for visible human flaws, unedited stammering, and raw acoustic texture in response to AI perfection.",
                "discussions": "Suspicion of flawless generative text and images; vocal fry and mid-sentence hesitations as proofs of humanity.",
                "artifacts": "One-take conversational podcasts, handwritten signatures, acoustic room reverb recordings.",
                "angle": "Proof of Humanity: Why Imperfection Became the Ultimate Digital Luxury.",
            },
            {
                "id": 65,
                "title": "Uncurated Close-Friends Culture & Photo Dumps",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 92.0,
                "engagement": 91.0,
                "hook": "Sharing blurry, unedited 10-photo monthly dumps exclusively to green-circle 'Close Friends' lists.",
                "discussions": "The collapse of the aspirational Instagram feed; posting half-eaten sandwiches and weird street signs; anti-glamour.",
                "artifacts": "Instagram Close Friends lists, unedited camera roll dumps, meme screenshot carousels.",
                "angle": "The Photo Dump Manifesto: How Gen Z Buried the Aspirational Grid.",
            },
            {
                "id": 66,
                "title": "The Flight from LinkedIn Cringe",
                "vibe_index": "Dialectical Backlash",
                "velocity": 89.5,
                "engagement": 93.0,
                "hook": "Communities mocking performative LinkedIn thought leadership, toxic hustle flexes, and fabricated moral stories.",
                "discussions": "r/LinkedInCringe memes; transparent tech layoff discussions; rejecting corporate jargon and forced optimism.",
                "artifacts": "Satirical 'What B2B Sales Taught Me About My Dog' parody posts, verified salary spreadsheets.",
                "angle": "The LinkedIn Parody Wave: Breaking Down Corporate Theater on the Professional Web.",
            },
            {
                "id": 67,
                "title": "Decentralized Social Protocol Curiosity (Nostr, Bluesky, Mastodon)",
                "vibe_index": "Underground Simmering",
                "velocity": 87.0,
                "engagement": 91.0,
                "hook": "Tech natives experimenting with federated social graphs and cryptographic identity to avoid platform lock-in.",
                "discussions": "The AT Protocol vs. ActivityPub; portable follower graphs; sovereign cryptographic keys (Nostr).",
                "artifacts": "Bluesky custom feeds, Nostr private keys, Mastodon server instances.",
                "angle": "The Federated Web: Why Decentralized Social Protocols Are Quietly Winning Developers.",
            },
            {
                "id": 68,
                "title": "Niche Forum Renaissance",
                "vibe_index": "Underground Simmering",
                "velocity": 85.5,
                "engagement": 92.5,
                "hook": "Users returning to classic Discourse and phpBB forums dedicated exclusively to espresso, mechanical keyboards, and fountain pens.",
                "discussions": "Avoiding Reddit moderation drama; threaded multi-year technical knowledge bases; high-signal discussions.",
                "artifacts": "Home-Barista forum accounts, Geekhack group-buy threads, member post count ranks.",
                "angle": "Return of the Forum: Why Specialized Hobbyists Are Abandoning Megaplatforms.",
            },
            {
                "id": 69,
                "title": "Micro-Events via Partiful & Luma",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.0,
                "engagement": 95.0,
                "hook": "Organizing casual rooftop hangs, park meetups, and trivia nights with playful SMS RSVPs and photo galleries.",
                "discussions": "The complete obsolescence of Facebook Events; phone-number RSVP loops; event-day attendee text blasts.",
                "artifacts": "Partiful RSVP guest lists with emojis, Luma QR calendar invites, party text blast chains.",
                "angle": "The New Party Architecture: How Partiful and Luma Rebuilt Local Event Culture.",
            },
            {
                "id": 70,
                "title": "Hyper-Specific Discord Study & Co-Working Lounges",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 90.0,
                "hook": "Virtual rooms where remote workers and students keep cameras on and mics muted for 8 hours of mutual focus.",
                "discussions": "Tackling remote work isolation; virtual body doubling for ADHD; Pomodoro break chat sessions.",
                "artifacts": "Muted webcams, Lofi Girl YouTube bot integrations, focus timer bots.",
                "angle": "Virtual Body Doubling: The Rise of 24/7 Silent Co-Working Rooms.",
            },
        ],
    },
    {
        "domain": "Workplace Realignment, Quiet Thriving & Craft",
        "icon": "🛠️",
        "topics": [
            {
                "id": 71,
                "title": "Quiet Thriving & Cortisol Management",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.0,
                "engagement": 94.0,
                "hook": "Moving beyond cynical 'quiet quitting' to intentionally structuring your workday around low stress, craft mastery, and peace.",
                "discussions": "Saying no to hollow promotions that double cortisol; setting unmovable boundaries; pride in doing good work calmly.",
                "artifacts": "Calendar blocks labeled 'Deep Work / No Meetings', hard 5:00 PM Slack logoffs, daily task limits.",
                "angle": "Quiet Thriving: The Art of Doing Great Work Without Sacrificing Your Nervous System.",
            },
            {
                "id": 72,
                "title": "Anti-Optimization Hobbyism",
                "vibe_index": "Dialectical Backlash",
                "velocity": 91.0,
                "engagement": 92.5,
                "hook": "Strictly refusing to monetize or optimize hobbies; taking up watercolor, pottery, or gardening purely for joyful leisure.",
                "discussions": "The tyranny of turning every creative interest into a side hustle; protecting leisure time as sacred.",
                "artifacts": "Imperfect clay pinch pots, unpainted watercolor sketchbooks, unfinished knit scarves.",
                "angle": "The Sacred Hobby: Why You Must Never Monetize Everything You Love.",
            },
            {
                "id": 73,
                "title": "Blue-Collar & Trade Apprenticeship Renaissance",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.5,
                "engagement": 95.0,
                "hook": "Gen Z turning away from white-collar desk jobs and tuition debt to become electricians, carpenters, and welders.",
                "discussions": "Tangible real-world results; high earning power without college debt; AI-proof physical trade careers.",
                "artifacts": "Tool belts, Klein electrical meters, trade school certifications, Carhartt work trousers.",
                "angle": "The Toolbelt Boom: Why Gen Z is Swapping Cubicles for Skilled Trades.",
            },
            {
                "id": 74,
                "title": "Async-First Remote Work Boundaries",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 91.0,
                "hook": "Replacing endless Zoom meetings with well-written asynchronous memos, Loom walkthroughs, and delayed notifications.",
                "discussions": "Calendar freedom; why most meetings could be a 3-paragraph markdown doc; eliminating instantaneous reply anxiety.",
                "artifacts": "3-minute Loom videos, Basecamp-style message boards, scheduled send email timers.",
                "angle": "The Async Manifesto: How to Eliminate 80% of Meetings Without Losing Alignment.",
            },
            {
                "id": 75,
                "title": "Sabbatical Normalization & Intentional Career Pauses",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 90.0,
                "hook": "Taking planned 3-to-6 month leaves in one's late 20s and 30s to travel, build open source, or reset mental health.",
                "discussions": "Budgeting for adult gap years; explaining employment gaps with pride on resumes; preventing complete career burnout.",
                "artifacts": "Sabbatical savings accounts, Notion travel roadmaps, open source side-project repos.",
                "angle": "The Mini-Retirement: Why Taking Sabbaticals in Your 30s Beats Retiring at 65.",
            },
            {
                "id": 76,
                "title": "Downshifting & Micro-Homesteading",
                "vibe_index": "Underground Simmering",
                "velocity": 86.0,
                "engagement": 92.0,
                "hook": "Exiting hyper-competitive metropolitan areas for small towns, tending backyard chickens, and planting raised vegetable beds.",
                "discussions": "Lowering baseline living costs; trading square footage for garden acreage; DIY home repairs.",
                "artifacts": "Cedar chicken coops, heirloom tomato stakes, rain barrels, canning jars.",
                "angle": "Downshifting: Escaping the Metro Rat Race for a Quarter-Acre Sanctuary.",
            },
            {
                "id": 77,
                "title": "Single-Tasking & Deep Work Monasticism",
                "vibe_index": "Dialectical Backlash",
                "velocity": 90.5,
                "engagement": 91.0,
                "hook": "Operating with only one browser tab open, full-screen apps, and airplane mode to execute 90 minutes of pure focus.",
                "discussions": "The cognitive cost of context switching; Cal Newport's Deep Work rules; closing 45 open browser tabs.",
                "artifacts": "Freedom / Cold Turkey app blockers, mechanical hourglass timers, noise-canceling headphones.",
                "angle": "The One-Tab Rule: How Single-Tasking Doubled My Engineering Output.",
            },
            {
                "id": 78,
                "title": "Corporate Absurdism & Anti-Jargon Parody",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.0,
                "engagement": 93.5,
                "hook": "Viral comedy sketches decoding passive-aggressive corporate emails ('per my previous email', 'let's circle back').",
                "discussions": "The comedy of corporate performance; exposing empty buzzwords; coping with existential knowledge worker absurdity.",
                "artifacts": "Corporate jargon bingo cards, satirical email templates, TikTok sketch series.",
                "angle": "Circling Back: How Corporate Jargon Satire Became the Internet's Favorite Comedy.",
            },
            {
                "id": 79,
                "title": "Portfolio Careers & Fractional Solopreneurship",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.0,
                "engagement": 90.0,
                "hook": "Ditching single full-time employers to assemble an agile mosaic of fractional advising, software products, and content.",
                "discussions": "Diversifying income streams; setting your own hourly rates; autonomy over career roadmap.",
                "artifacts": "Stripe payout dashboards, LLC business filings, modular client advisory contracts.",
                "angle": "The Fractional Professional: Building a Resilient Multi-Stream Income Stack.",
            },
            {
                "id": 80,
                "title": "The 4-Day Workweek Experimenters",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.5,
                "engagement": 93.0,
                "hook": "Companies and teams standardizing 32-hour, 4-day workweeks with zero pay reduction, proving equal or higher productivity.",
                "discussions": "Results from global 4-day week trials; Friday wellness days; eliminating useless administrative meetings.",
                "artifacts": "32-hour scheduling calendars, 4-Day Week Global trial studies, automated Friday out-of-office responders.",
                "angle": "The 32-Hour Frontier: Inside Companies That Successfully Cut Fridays.",
            },
        ],
    },
    {
        "domain": "Food & Beverage Rituals, Slow Consumption & Fermentation",
        "icon": "🍞",
        "topics": [
            {
                "id": 81,
                "title": "Wild Sourdough & Heirloom Grain Milling",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 92.0,
                "hook": "Stone-milling heritage Einkorn and Spelt wheat berries at home to bake 80% hydration open-crumb sourdough loaves.",
                "discussions": "Fermentation microbial diversity; scoring patterns and oven spring; digestibility of long-fermented grains.",
                "artifacts": "Mockmill stone grain mills, Challenger bread pans, rattan bannetons, sourdough starter jars.",
                "angle": "Heirloom Loaves: The Science and Craft of Home Grain Milling.",
            },
            {
                "id": 82,
                "title": "Home Fermentation & Koji Alchemy",
                "vibe_index": "Underground Simmering",
                "velocity": 87.0,
                "engagement": 93.5,
                "hook": "Cultivating Aspergillus oryzae (koji mold) on barley to brew artisanal shoyu, lacto-fermented hot sauces, and misos.",
                "discussions": "The Noma Guide to Fermentation; koji chamber humidity control; umami flavor unlocking.",
                "artifacts": "Cedar fermentation trays, inkbird temperature controllers, airlock mason jars, sea salt refractometers.",
                "angle": "Koji Alchemy: How Home Cooks Are Unlocking Five-Star Umami Flavors.",
            },
            {
                "id": 83,
                "title": "Single-Dose Specialty Espresso & Bean Freezing",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.0,
                "engagement": 95.0,
                "hook": "Weighing single-origin light roast coffee beans to 0.1g, freezing vacuum tubes, and using needle WDT distribution tools.",
                "discussions": "James Hoffmann extraction science; blind shaker distribution vs. WDT; freezing beans to halt degassing.",
                "artifacts": "Acaia Lunar precision scales, Weber Workshops key grinders, centrifuge coffee bean freezer tubes.",
                "angle": "The 0.1-Gram Coffee Ritual: Inside the World of Extreme Espresso Precision.",
            },
            {
                "id": 84,
                "title": "Adaptogenic Mocktails & Functional Aperitifs",
                "vibe_index": "Hyper-Surging",
                "velocity": 92.0,
                "engagement": 90.5,
                "hook": "Crafting sophisticated bitter evening cocktails using botanical distillates, ashwagandha, L-theanine, and gentian root.",
                "discussions": "Replacing the evening wine unwind; craft zero-proof mixology; Ghia, De Soi, and botanical bitters.",
                "artifacts": "Heavy coupe cocktail glasses, large clear ice cube molds, bar jiggers, botanical bitter dropper bottles.",
                "angle": "The Functional Hour: How to Craft World-Class Mocktails with Real Botanicals.",
            },
            {
                "id": 85,
                "title": "Tinned Fish & Conservas Gourmet Culture",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.5,
                "engagement": 93.0,
                "hook": "Curating high-end Iberian tinned seafood (spiced sardines, razor clams in brine, smoked mussels) for charcuterie boards.",
                "discussions": "Spanish and Portuguese conservas history; pairing tinned seafood with potato chips and vermouth; pantry luxury.",
                "artifacts": "Artisanal illustrated sardine tins, wooden serving boards, cocktail toothpicks, pickled guindilla peppers.",
                "angle": "The Conservas Renaissance: Why Gourmet Tinned Fish Became a Modern Luxury.",
            },
            {
                "id": 86,
                "title": "Ceremonial Matcha Whisking Ceremonies",
                "vibe_index": "Hyper-Surging",
                "velocity": 95.0,
                "engagement": 96.0,
                "hook": "Whisking single-cultivar stone-ground green tea powder from Uji in handcrafted ceramic chawan bowls with bamboo chasens.",
                "discussions": "Ceremonial grade vs. culinary grade matcha; L-theanine calming focus; whisking the perfect microfoam foam layer.",
                "artifacts": "Bamboo 100-prong chasen whisks, ceramic chawan bowls, stainless mesh sifters, oat milk micro-foam steamers.",
                "angle": "The Matcha Ritual: How 800 Years of Zen Tea Culture Conquered Morning Routines.",
            },
            {
                "id": 87,
                "title": "Farm-to-Table CSAs & Regenerative Meat Shares",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 91.0,
                "hook": "Buying whole-animal grass-fed beef quarters and weekly heirloom produce boxes directly from local regenerative farms.",
                "discussions": "Soil microbiome health; rotational grazing and carbon sequestration; cooking nose-to-tail cuts.",
                "artifacts": "Deep chest freezers, vacuum sealers, weekly wooden CSA produce crates.",
                "angle": "The Meat Share Movement: How Buying Directly from Regenerative Ranches Outsmarts Supermarkets.",
            },
            {
                "id": 88,
                "title": "Raw Honey & Single-Origin Hive Sourcing",
                "vibe_index": "Underground Simmering",
                "velocity": 85.0,
                "engagement": 89.0,
                "hook": "Tasting single-origin unheated raw honey with terroir notes ranging from mountain wildflower to sourwood and buckwheat.",
                "discussions": "Enzymes in unpasteurized honey; backyard beekeeping setups; combating adulterated commercial honey.",
                "artifacts": "Raw honeycomb squares, wooden honey dippers, Mason jars with pollen granules.",
                "angle": "Terroir in a Jar: Why Raw Single-Origin Honey is the New Craft Wine.",
            },
            {
                "id": 89,
                "title": "Zero-Waste Root-to-Stem Cooking",
                "vibe_index": "Underground Simmering",
                "velocity": 86.5,
                "engagement": 88.5,
                "hook": "Pickling watermelon rinds, blending carrot top pestos, and simmering onion skins into mineral-rich umami broths.",
                "discussions": "Cooking sustainably without waste; creative culinary economy; stretching groceries 40% further.",
                "artifacts": "Pickling brine crocks, vegetable scrap freezer bags, immersion blenders.",
                "angle": "Root to Stem: Delicious, Zero-Waste Recipes from Kitchen Scraps.",
            },
            {
                "id": 90,
                "title": "Traditional Herbal Infusions & Wild Tisanes",
                "vibe_index": "Underground Simmering",
                "velocity": 84.0,
                "engagement": 88.0,
                "hook": "Steeping whole dried chamomile flowers, stinging nettle, and foraged pine needles into restorative non-caffeinated brews.",
                "discussions": "Herbalism traditions; steeping times for medicinal roots; foraging spruce tips in early spring.",
                "artifacts": "Glass teapot infusers, dried whole chamomile flowers, stainless mesh tea balls.",
                "angle": "The Wild Apothecary: How to Brew Medicinal Herbal Tisanes at Home.",
            },
        ],
    },
    {
        "domain": "Urbanism, Tactile Transport & Micro-Mobility",
        "icon": "🚲",
        "topics": [
            {
                "id": 91,
                "title": "Bikepacking & Gravel Cycling Escapes",
                "vibe_index": "Hyper-Surging",
                "velocity": 94.0,
                "engagement": 95.5,
                "hook": "Strapping ultralight tents to wide-tire gravel bikes for self-supported weekend bikepacking adventures off-grid.",
                "discussions": "Wide tire tubeless setups; custom Cordura frame bags; escaping traffic onto logging and fire roads.",
                "artifacts": "Tubeless gravel tires, Ortlieb frame packs, titanium camp stoves, ultralight bivy sacks.",
                "angle": "The Gravel Bikepacking Revolution: Everything You Need for Your First Off-Grid Cycling Overnight.",
            },
            {
                "id": 92,
                "title": "Pedestrian Urbanism & 15-Minute Cities",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 90.0,
                "engagement": 94.0,
                "hook": "Advocating for bollards, daylighted intersections, protected bike lanes, and car-free pedestrian commercial corridors.",
                "discussions": "Not Just Bikes urbanist YouTube channels; child-friendly street designs; revitalizing local corner bodegas.",
                "artifacts": "Walk Score dashboards, protected concrete bike lane dividers, pedestrian plaza street furniture.",
                "angle": "Cities for People: The Worldwide Grassroots Movement to Reclaim Streets from Cars.",
            },
            {
                "id": 93,
                "title": "Slow Train Travel & Nightjet Sleeper Revival",
                "vibe_index": "Hyper-Surging",
                "velocity": 92.5,
                "engagement": 93.0,
                "hook": "Choosing overnight European sleeper trains (Nightjet) and scenic Amtrak routes over stressful airport security lines.",
                "discussions": "Watching landscapes pass by train windows; dining cars as romantic social spaces; low-carbon travel alternatives.",
                "artifacts": "Sleeper car bunk tickets, Eurail passes, compact travel toiletry rolls, paperback books.",
                "angle": "The Sleeper Train Renaissance: Why Slow Rail Travel Conquered Europe.",
            },
            {
                "id": 94,
                "title": "Compact Cargo E-Bikes for Family Transit",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 91.0,
                "engagement": 92.0,
                "hook": "Urban families replacing second cars with longtail electric cargo bicycles capable of carrying two kids and groceries.",
                "discussions": "Bypassing school drop-off traffic; Bosch mid-drive electric motors; winter studded bike tires.",
                "artifacts": "Tern GSD cargo bikes, rear child carrier seats, waterproof panniers, heavy ABUS chain locks.",
                "angle": "The Two-Wheeled Family Car: How Cargo E-Bikes Are Transforming Suburban Parenting.",
            },
            {
                "id": 95,
                "title": "Skateboarding & Surfskate Urban Commuting",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 87.5,
                "engagement": 89.0,
                "hook": "Commuting through city streets on carving surfskates (Carver, YOW) that replicate wave-riding mechanics on asphalt.",
                "discussions": "Front truck pivoting mechanics; carving sidewalk transitions; turning daily transit into core exercise.",
                "artifacts": "Carver surfskate trucks, 70mm soft urethane wheels, Canadian maple decks.",
                "angle": "Surfing the Concrete: How Surfskating Revolutionized Urban Street Transit.",
            },
            {
                "id": 96,
                "title": "Kei Van & Minimalist Camper Conversions",
                "vibe_index": "Hyper-Surging",
                "velocity": 93.0,
                "engagement": 94.5,
                "hook": "Importing tiny 660cc Japanese Kei vans (Daihatsu Hijet, Subaru Sambar) and converting them into micro-campers.",
                "discussions": "Japanese Kei vehicle 25-year import rules; 45 MPG micro-footprints; building custom birch plywood bed platforms.",
                "artifacts": "Right-hand drive Kei vans, fold-flat wooden sleeping platforms, portable Jackery power stations.",
                "angle": "The Kei Camper Craze: Why Tiny Japanese Vans Are the Ultimate Weekend Freedom Machines.",
            },
            {
                "id": 97,
                "title": "Tactile Titanium Everyday Carry (EDC) Gear",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 88.0,
                "engagement": 91.0,
                "hook": "Curating minimalist, indestructible pocket carry tools: titanium pry bars, bolt-action pens, and key organizers.",
                "discussions": "CNC-machined titanium finishes; eliminating bulky jangling keychains; fidget mechanics in functional gear.",
                "artifacts": "Big Idea Design bolt-action pens, KeyBar organizers, Olight micro flashlights, titanium prybars.",
                "angle": "The Minimalist Pocket: How Tactile EDC Gear Built a Massive Cult Following.",
            },
            {
                "id": 98,
                "title": "Dead Mall Walking & Urban Exploration (Urbex)",
                "vibe_index": "Underground Simmering",
                "velocity": 86.0,
                "engagement": 90.0,
                "hook": "Exploring, photographing, and mourning fading 1980s enclosed shopping malls, neon fountains, and abandoned department stores.",
                "discussions": "Dan Bell's Dead Mall Series; the architectural death of retail suburban centers; consumer archeology.",
                "artifacts": "Wide-angle prime lenses, flashlight beams, nostalgic mall directory scans, vaporwave soundtracks.",
                "angle": "Mall of the Dead: What Abandoned Shopping Centers Reveal About Consumer History.",
            },
            {
                "id": 99,
                "title": "Neighborhood Open Streets & Block Parties",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 89.0,
                "engagement": 91.0,
                "hook": "Coordinating Sunday municipal permits to shut down streets to motor vehicles, opening asphalt to chalk, scooters, and music.",
                "discussions": "Building neighbor friendships; children playing freely on streets; transforming thoroughfares into public living rooms.",
                "artifacts": "Sawhorse street barriers, sidewalk chalk buckets, porch acoustic guitars, folding lawn chairs.",
                "angle": "Reclaiming the Asphalt: The Explosive Growth of Open Street Sundays.",
            },
            {
                "id": 100,
                "title": "Community Tool Libraries & Shared Workshops",
                "vibe_index": "Mainstream Infiltration",
                "velocity": 87.0,
                "engagement": 90.5,
                "hook": "Checking out lawn mowers, table saws, and pressure washers from neighborhood tool libraries instead of individually purchasing them.",
                "discussions": "De-duplicating consumer garage junk; enabling DIY home improvement for renters; volunteer tool sharpening.",
                "artifacts": "Tool library barcode tags, Makita cordless drills, Bosch table saws, tool donation bins.",
                "angle": "The Tool Library Movement: Why Borrowing Beats Owning for Modern DIYers.",
            },
        ],
    },
]


def get_all_100_topics() -> List[Dict[str, Any]]:
    """Returns the flattened, numbered list of all 100 zeitgeist topics."""
    flat_list = []
    for domain_group in ZEITGEIST_DOMAINS:
        domain_name = domain_group["domain"]
        domain_icon = domain_group.get("icon", "📌")
        for topic in domain_group["topics"]:
            t_copy = dict(topic)
            t_copy["domain"] = domain_name
            t_copy["domain_icon"] = domain_icon
            flat_list.append(t_copy)
    return flat_list


def generate_top_100_split_reports() -> tuple[str, str]:
    """
    Renders the comprehensive 100-topic dossier split into:
    - Part 1 (Issue Body): Executive Summary, Master Table (all 100 topics), Domains 1-5 (Topics 1-50)
    - Part 2 (Issue Comment): Domains 6-10 (Topics 51-100), Tactical Creator Synthesis
    This ensures complete in-depth coverage while adhering to GitHub's 65KB issue body limit.
    """
    now_dt = datetime.now(timezone.utc)
    date_str = now_dt.strftime("%Y-%m-%d")

    # Build Part 1 (Issue Body)
    p1 = [
        f"# 🌍 The Cultural Zeitgeist 100: Top Niche Subcultures, Anti-Trends & Social Shifts (2026 Edition)",
        f"> **Curated by [Market Research](https://github.com/holman57/market-research) & Orchestrated by [Adrastea](https://github.com/holman57/Adrastea)**",
        "",
        "| Metric | Value | Primary Trend Pulse | Edition Date |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Total Curated Niches** | `100 Topics` | *Tactile Realism, Human Imperfection & Intentional Friction* | `{date_str}` |",
        "",
        "---",
        "",
        "## 🧭 Executive Cultural Overview: The Great Dialectical Turn",
        "The contemporary cultural zeitgeist is defined by a massive, dialectical counter-reaction against ",
        "**algorithmic homogeny, hyper-convenient digital frictionlessness, and synthetic AI perfection**. ",
        "Across every sector—from communication and fashion to food, fitness, and entertainment—individuals are ",
        "actively reclaiming **tangible reality, physical communities, human flaws, and intentional friction**.",
        "",
        "### 🔑 The 4 Macro Currents Driving the 100 Niches:",
        "1. **The Hunger for Tactile Resistance:** Dumbing down phones, shooting on CCD digicams, writing in paper notebooks, and listening to vinyl.",
        "2. **The Re-Engineering of the Third Place:** Gathering for silent reading parties, run clubs, supper clubs, and sauna circles to combat atomization.",
        "3. **Underconsumption & De-influencing:** Shifting status from owning new things to wearing resoled boots, using products to the pan, and mending garments.",
        "4. **Proof of Humanity:** Valuing conversational flaws, vocal stammering, and unscripted dialogue over synthetic, frictionless AI outputs.",
        "",
        "---",
        "",
        "## 📑 Master Directory Table (All 100 Niches Across 10 Domains)",
        "| # | Niche Topic | Cultural Domain | Vibe Index | Velocity | Hook |",
        "| :---: | :--- | :--- | :---: | :---: | :--- |",
    ]

    for d in ZEITGEIST_DOMAINS:
        short_domain = d["domain"].split(" & ")[0]
        for t in d["topics"]:
            p1.append(f"| {t['id']} | **{t['title']}** | {short_domain} | `{t['vibe_index']}` | `{t['velocity']}` | {t['hook']} |")

    p1.extend([
        "",
        "---",
        "",
        "## 📖 Part 1: Deep Dive Breakdown — Domains 1 to 5 (Topics 1–50)",
        "",
    ])

    for d_idx, domain_group in enumerate(ZEITGEIST_DOMAINS[:5], 1):
        domain_name = domain_group["domain"]
        icon = domain_group.get("icon", "📌")
        p1.extend([
            f"### Domain {d_idx}: {icon} {domain_name}",
            f"*Comprehensive analysis of topics {(d_idx - 1) * 10 + 1} to {d_idx * 10}.*",
            "",
        ])
        for topic in domain_group["topics"]:
            t_id = topic["id"]
            badge = f"`Status: {topic['vibe_index']}` | `Velocity: {topic['velocity']}/100` | `Engagement: {topic['engagement']}/100`"
            p1.extend([
                f"#### #{t_id}. {topic['title']}",
                f"{badge}",
                "",
                f"> *\"{topic['hook']}\"*",
                "",
                f"- **🗣️ What People Are Dissecting & Discussing:** {topic['discussions']}",
                f"- **🎒 Tangible Artifacts & Participation Rituals:** {topic['artifacts']}",
                f"- **💡 Content & Spawning System Angle:** `{topic['angle']}`",
                "",
                "---",
                "",
            ])

    p1.extend([
        "",
        "> 💡 **Continued Below in Issue Comment:** Detailed Breakdown of **Domains 6 through 10 (Topics 51–100)** and the **Tactical Creator Playbook**.",
        "",
    ])

    # Build Part 2 (Issue Comment)
    p2 = [
        f"# 🌍 Part 2: Detailed Cultural Breakdown — Domains 6 to 10 (Topics 51–100)",
        f"> *Continuation of [Cultural Zeitgeist 100](https://github.com/holman57/market-research) (Edition {date_str})*",
        "",
        "---",
        "",
    ]

    for d_idx, domain_group in enumerate(ZEITGEIST_DOMAINS[5:], 6):
        domain_name = domain_group["domain"]
        icon = domain_group.get("icon", "📌")
        p2.extend([
            f"### Domain {d_idx}: {icon} {domain_name}",
            f"*Comprehensive analysis of topics {(d_idx - 1) * 10 + 1} to {d_idx * 10}.*",
            "",
        ])
        for topic in domain_group["topics"]:
            t_id = topic["id"]
            badge = f"`Status: {topic['vibe_index']}` | `Velocity: {topic['velocity']}/100` | `Engagement: {topic['engagement']}/100`"
            p2.extend([
                f"#### #{t_id}. {topic['title']}",
                f"{badge}",
                "",
                f"> *\"{topic['hook']}\"*",
                "",
                f"- **🗣️ What People Are Dissecting & Discussing:** {topic['discussions']}",
                f"- **🎒 Tangible Artifacts & Participation Rituals:** {topic['artifacts']}",
                f"- **💡 Content & Spawning System Angle:** `{topic['angle']}`",
                "",
                "---",
                "",
            ])

    p2.extend([
        "## 🚀 Tactical Synthesis for Creators & Content Engines",
        "1. **Never Sell Frictionless Ease:** Audiences are cynical about effortless solutions. Emphasize craftsmanship, patience, and visible labor.",
        "2. **Feature the Scars:** In product reviews and lifestyle media, highlight longevity, repairability, and patina over shiny newness.",
        "3. **Build Kinship, Not Just Broadcasts:** Pair content feeds with real-world meetups, Discord salons, or localized rituals.",
        "4. **Embrace Skeuomorphism & Warmth:** Visual content should lean into tactile textures, Frutiger Aero optimism, and direct-flash photography.",
        "",
        "---",
        "*Automated zeitgeist intelligence compiled by [Market Research](https://github.com/holman57/market-research) & orchestrated by [Adrastea](https://github.com/holman57/Adrastea).*",
    ])

    return "\n".join(p1), "\n".join(p2)


def generate_top_100_markdown_report() -> str:
    """Returns the unified 100-topic markdown dossier."""
    p1, p2 = generate_top_100_split_reports()
    return f"{p1}\n\n---\n\n{p2}"


def post_top_100_zeitgeist_issue(
    repo: str = "holman57/market-research",
    assignee: str = "holman57",
    issue_title: str = "[Cultural Zeitgeist] Top 100 Niche Topics & Subcultures in the Cultural Zeitgeist (2026 Edition)",
) -> Dict[str, Any]:
    """
    Creates or updates the dedicated Top 100 Zeitgeist issue on holman57/market-research.
    - If the issue does not exist: creates it with Part 1 and posts Part 2 as an immediate comment.
    - If the issue exists: updates the issue description with Part 1 and appends Part 2 as an updated comment.
    """
    part1_body, part2_comment = generate_top_100_split_reports()

    # Search for existing issue
    search_cmd = [
        "gh", "issue", "list",
        "--repo", repo,
        "--state", "open",
        "--json", "number,title,url",
    ]
    try:
        res = subprocess.run(
            search_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        issues = json.loads(res.stdout) if res.stdout.strip() else []
    except Exception as e:
        logger.warning(f"Failed to query issues on {repo}: {e}")
        issues = []

    target_issue = None
    for iss in issues:
        title = iss.get("title", "")
        if "Top 100 Niche Topics" in title or "[Cultural Zeitgeist] Top 100" in title:
            target_issue = iss
            break

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".md", delete=False) as f1:
        f1.write(part1_body)
        part1_path = f1.name

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".md", delete=False) as f2:
        f2.write(part2_comment)
        part2_path = f2.name

    try:
        if target_issue:
            issue_number = target_issue["number"]
            issue_url = target_issue.get("url", f"https://github.com/{repo}/issues/{issue_number}")
            logger.info(f"Updating existing Top 100 Zeitgeist issue #{issue_number} on {repo}")

            # Update body with Part 1
            subprocess.run(
                ["gh", "issue", "edit", str(issue_number), "--repo", repo, "--body-file", part1_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )

            # Append Part 2 comment
            subprocess.run(
                ["gh", "issue", "comment", str(issue_number), "--repo", repo, "--body-file", part2_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )

            return {
                "action": "updated",
                "repo": repo,
                "issue_number": issue_number,
                "issue_url": issue_url,
            }

        else:
            logger.info(f"Creating new Top 100 Zeitgeist issue on {repo}")
            create_cmd = [
                "gh", "issue", "create",
                "--repo", repo,
                "--title", issue_title,
                "--body-file", part1_path,
                "--label", "documentation",
            ]
            if assignee:
                create_cmd.extend(["--assignee", assignee])

            res = subprocess.run(
                create_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )
            created_url = res.stdout.strip()
            m = re.search(r"/issues/(\d+)", created_url)
            issue_number = int(m.group(1)) if m else None

            # Add Part 2 as the immediate first comment
            if issue_number:
                subprocess.run(
                    ["gh", "issue", "comment", str(issue_number), "--repo", repo, "--body-file", part2_path],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=True,
                )

            return {
                "action": "created",
                "repo": repo,
                "issue_number": issue_number,
                "issue_url": created_url,
            }
    finally:
        for p in (part1_path, part2_path):
            try:
                os.remove(p)
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description="Cultural Zeitgeist Top 100 Niche Intelligence")
    parser.add_argument("--post", action="store_true", help="Post or update the Top 100 issue on GitHub")
    parser.add_argument("--repo", default="holman57/market-research", help="Target GitHub repository")
    parser.add_argument("--assignee", default="holman57", help="Issue assignee handle")
    parser.add_argument("-o", "--output", default=None, help="Save markdown dossier to file")
    parser.add_argument("--stdout", action="store_true", help="Print report markdown to stdout")
    args = parser.parse_args()

    if args.post:
        print(f"[*] Posting Top 100 Zeitgeist Topics issue to {args.repo}...")
        res = post_top_100_zeitgeist_issue(repo=args.repo, assignee=args.assignee)
        print(f"[+] Result: {res}")
        return

    md = generate_top_100_markdown_report()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[+] Written report to: {args.output}")

    if args.stdout or not args.output:
        print(md)


if __name__ == "__main__":
    main()
