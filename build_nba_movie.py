import os
import subprocess
import yt_dlp

# The Most Impactful Storylines of the 2025-2026 NBA Season
MOMENTS = [
    {"title": "01_Tatum_Return", "query": "ytsearch1:Jayson Tatum return game highlights 2025 2026 NBA"},
    {"title": "02_Thunder_Nuggets_OT", "query": "ytsearch1:Thunder vs Nuggets overtime full game highlights 2025 2026"},
    {"title": "03_Bam_Adebayo_83_Points", "query": "ytsearch1:Bam Adebayo 83 points highlights Wizards Heat"},
    {"title": "04_Cooper_Flagg_50_Points_ROTY", "query": "https://www.youtube.com/watch?v=8x33WkvTnhw"},
    {"title": "05_2026_Trade_Deadline_Recap", "query": "ytsearch1:Trae Young Anthony Davis Jaren Jackson Jr trade deadline 2026 NBA"},
    {"title": "06_SGA_Historic_Streak", "query": "ytsearch1:Shai Gilgeous Alexander historic 20 point streak highlights 2026"},
    {"title": "07_Best_Game_Winners_2026", "query": "ytsearch1:NBA 2025-26 season best buzzer beaters game winners"},
    {"title": "08_Sixers_Upset_Celtics", "query": "https://www.youtube.com/watch?v=DJYyZAxulTM"},
    {"title": "09_Cavs_Upset_1Seed_Pistons", "query": "https://www.youtube.com/watch?v=51C1_EzTueA"},
    {"title": "10_Wemby_Spurs_Dethrone_Thunder", "query": "https://www.youtube.com/watch?v=1bOMYQFgK4I"},
    {"title": "11_Finals_Game4_29Pt_Comeback", "query": "https://www.youtube.com/watch?v=4WzuI2GntPc"},
    {"title": "12_OG_Anunoby_Iconic_Game4_TipIn", "query": "https://www.youtube.com/watch?v=sOQKRjP3ZJk"},
    {"title": "13_Brunson_45Pts_Knicks_Title", "query": "https://www.youtube.com/watch?v=mQPbdoRZYY8"},
]

os.makedirs("clips", exist_ok=True)
concat_list = []

for idx, item in enumerate(MOMENTS):
    out_tmpl = f"clips/clip_{idx:02d}.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': out_tmpl,
        'merge_output_format': 'mp4',
        'quiet': False,
        'ignoreerrors': True,
        'match_filter': yt_dlp.utils.match_filter_func("duration < 900"),
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }
    print(f"Downloading {item['title']}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([item['query']])

    expected_file = f"clips/clip_{idx:02d}.mp4"
    if os.path.exists(expected_file):
        norm_file = f"clips/norm_{idx:02d}.ts"
        cmd = [
            "ffmpeg", "-y", "-i", expected_file,
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "128k",
            "-f", "mpegts", norm_file
        ]
        subprocess.run(cmd, check=True)
        concat_list.append(norm_file)

if concat_list:
    concat_str = "concat:" + "|".join(concat_list)
    final_cmd = [
        "ffmpeg", "-y", "-i", concat_str,
        "-c", "copy", "-bsf:a", "aac_adtstoasc",
        "NBA_2025_2026_Impactful_Moments.mp4"
    ]
    subprocess.run(final_cmd, check=True)
    print("Movie successfully built: NBA_2025_2026_Impactful_Moments.mp4")
