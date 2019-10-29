import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tempfile
import textwrap

from subassert import convert_file


def test_subassert_regular():
    source_ass = textwrap.dedent('''
        [Script Info]
        ; Test subtitles
        Title: Test
        ScriptType: v4.00+
        Collisions: Normal
        PlayDepth: 0

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: DefaultVCD, Arial,28,&H00B4FCFC,&H00B4FCFC,&H00000008,&H80000008,-1,0,0,0,100,100,0.00,0.00,1,1.00,2.00,2,30,30,30,0

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        Dialogue: 0,0:00:01.18,0:00:06.85,Default, NTP,0000,0000,0000,,{\pos(400,570)}The line
    ''')
    source_file = tempfile.NamedTemporaryFile(delete=False)
    source_file.write(source_ass.encode('utf-8'))
    source_file.close()

    lines = list(convert_file(source_file.name, ''))
    assert lines == [
        '1\n00:00:01,180 --> 00:00:06,850\nThe line\n'
    ]
