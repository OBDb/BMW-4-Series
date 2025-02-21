import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.can_frame import CANIDFormat
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_testrunner

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    # TODO: Implement real tests below with vehicle data.
    # 2019 model year
    {
        "model_year": "2019",
        "signalset": "default.json",
        "tests": [
            ("60DF106621000000000", {"UNK_1000": 0}),

            ("""60DF1100B6220008017
                60DF1217C6C0D100E6D""", {"UNK_2000": 128}),

            ("""60DF110256220010080
                60DF121177C6C021700
                60DF12201373F17010B
                60DF123076BF3170001
                60DF1247AB317010C47
                60DF1258BD401000219
                60DF1260300FFFFFFFF""", {"UNK_2001": 0}),

            ("""60DF1101A622002000D
                60DF121100E6D011700
                60DF122014B4F17010B
                60DF1235E7B0B010002
                60DF124010300FFFFFF""", {"UNK_2002": 0}),

            ("""60DF1100F622504003C
                60DF121002000200001
                60DF122000A000AFFFF""", {"UNK_2504": 0}),

            ("""60DF1101D6230010100
                60DF121040064008202
                60DF1228A2710000500
                60DF12308028A271000
                60DF124050008000000""", {"UNK_3001": 1}),

            ("""60DF110096230021803
                60DF12100000000FFFF""", {"UNK_3002": 24}),

            ("""60DF1100A6230045A0A
                60DF1211C3E464F64FF""", {"UNK_3004": 90}),

            ("""60DF110096230050203
                60DF12100000000FFFF""", {"UNK_3005": 2}),
                
            ("""60DF110096230060200
                60DF12100000000FFFF""", {"UNK_3006": 2}),
                
            ("""60DF110096230070201
                60DF12100000000FFFF""", {"UNK_3007": 2}),
                
            ("""60DF110096230080202
                60DF12100000000FFFF""", {"UNK_3008": 2}),
                
            ("""60DF110096230090B01
                60DF12100000000FFFF""", {"UNK_3009": 11}),
                
            ("""60DF1100962300A0800
                60DF12100000000FFFF""", {"UNK_300A": 8}),
                
            ("""60DF1100962300B0202
                60DF121051401F4FFFF""", {"UNK_300B": 2}),
                
            ("""60DF1100962300C0303
                60DF12100000000FFFF""", {"UNK_300C": 3}),
                
            ("""60DF1100862300D0100
                60DF12178006EFFFFFF""", {"UNK_300D": 1}),
                
            ("""60DF1103E62300E4074
                60DF1213E8021342328
                60DF12240743E802134
                60DF1232328000DAC0D
                60DF124AC4844000004
                60DF125B00000000000
                60DF126040008002000
                60DF127400800100040
                60DF128008000008004
                60DF129000002000102
                60DF12A000100FFFFFF""", {"UNK_300E": 64}),
                
            ("""60DF110676230110000
                60DF12100FA00FA015E
                60DF122000000000000
                60DF123000000000000
                60DF124000000000200
                60DF125000046009601
                60DF1265E0000000000
                60DF127000000000000
                60DF128000000000002
                60DF1290000006400C8
                60DF12A019000000000
                60DF12B000000000000
                60DF12C000000000000
                60DF12D02000000FA00
                60DF12EFA0190000000
                60DF12F000000000000
                60DF120000000000000
                60DF1210002FFFFFFFF""", {"UNK_3011": 0}),
                
            ("""60DF1102D623016008F
                60DF121000000640000
                60DF122008F000A0002
                60DF123050000004B00
                60DF12455010E000500
                60DF12505000A01F400
                60DF1260A001E000300
                60DF127001401F4FFFF""", {"UNK_3016": 0}),
                
            ("""60DF11039623018E0FF
                60DF1210F00640A094B
                60DF122094B094B0796
                60DF12396640F0F026B
                60DF12461A8C3503C01
                60DF125F40A07D03A98
                60DF126520807501388
                60DF127000000000000
                60DF128000A000A2710
                60DF1290032000AFFFF""", {"UNK_3018": 224}),
                
            ("""60DF1100A62301E0F00
                60DF121050014012CFF""", {"UNK_301E": 15}),
                
            ("""60DF1101862301F0F27
                60DF121100A0A0A0A17
                60DF1227001F45050C8
                60DF1234000280A5014
                60DF12417FFFFFFFFFF""", {"UNK_301F": 15}),
                
            ("""60DF110086230200126
                60DF1211B010EFFFFFF""", {"UNK_3020": 1}),
                
            ("""60DF110CF6230212710
                60DF121015527100155
                60DF1224E2003FF4E20
                60DF12303FF01000148
                60DF12408001B01020D
                60DF1250EFF190C0221
                60DF1260FF815090258
                60DF12713F8120402BC
                60DF12817FB0F020384
                60DF1291BFD0F0003E8
                60DF12A1CFF0E00044C
                60DF12B1CFF0E0004E2
                60DF12C1C000E00055F
                60DF12D1C00172B0400
                60DF12E2134271001F4
                60DF12F002006061E66
                60DF120FF0000000000
                60DF121000000000019
                60DF12213202D0E213D
                60DF1232B0128122800
                60DF124280028002800
                60DF125280028002800
                60DF1262D002D002D00
                60DF1272D002D002D00
                60DF1282D002D002D00
                60DF129110D1957110D
                60DF12A1957110D1957
                60DF12B110D19570000
                60DF12C000996552B7F
                60DF12D7F7F0A801A03
                60DF12E050A9191553C
                60DF12F400F3D638000
                60DF120000000000000
                60DF121000000000000
                60DF12200000000FFFF""", {"UNK_3021": 39}),
                
            ("60DF10662D223000101", {"UNK_D223": 0}),
            
            ("60DF10562D23B0001", {"UNK_D23B": 0}),
            
            ("60DF10562D2400027", {"UNK_D240": 0}),
            
            ("60DF10562D24100FD", {"UNK_D241": 0}),
            
            ("60DF10562D2420000", {"UNK_D242": 0}),
            
            ("60DF10562D2430000", {"UNK_D243": 0}),
            
            ("60DF10562D2440000", {"UNK_D244": 0}),
            
            ("60DF10562D2450001", {"UNK_D245": 0}),
            
            ("60DF10562D2460000", {"UNK_D246": 0}),
            
            ("60DF10562D24C0001", {"UNK_D24C": 0}),
            
            ("60DF10562D3000001", {"UNK_D300": 0}),
            
            ("60DF10562D3030000", {"UNK_D303": 0}),
            
            ("""60DF1100A62D31C3C44
                60DF1212814110B0EFF""", {"UNK_D31C": 60}),
                
            ("""60DF1100B62D3770000
                60DF121000000000000""", {"UNK_D377": 0}),
                
            ("60DF10562D84A0000", {"UNK_D84A": 0}),
            
            ("""60DF1100762F1000181
                60DF1210001FFFFFFFF""", {"UNK_F100": 1}),
                
            ("""60DF1103462F1010101
                60DF12100041712088B
                60DF122009601000010
                60DF123000000010000
                60DF1242FA901000006
                60DF12500002FAD0900
                60DF1260108000041FD
                60DF127030803050000
                60DF1285710040000FF""", {"UNK_F101": 1}),
                
            ("""60DF1102C62F1020101
                60DF12100031712088B
                60DF122009601000010
                60DF123000000010000
                60DF1242FA901000006
                60DF12500002FAD0900
                60DF1260108000041FD
                60DF127030803FFFFFF""", {"UNK_F102": 1})
        ]
    },
]

def load_signalset(filename: str) -> str:
    """Load a signalset JSON file from the standard location."""
    signalset_path = REPO_ROOT / "signalsets" / "v3" / filename
    with open(signalset_path) as f:
        return f.read()

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    signalset_json = load_signalset(test_group["signalset"])

    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner(
                signalset_json,
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT,
                extended_addressing_enabled=True
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}, "
                f"Signalset: {test_group['signalset']}): {e}"
            )

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])
