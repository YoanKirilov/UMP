import speedtest
from tabulate import tabulate

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    ping = st.results.ping

    data = [["Download Speed", f"{download_speed:.2f} Mbps"],
            ["Upload Speed", f"{upload_speed:.2f} Mbps"],
            ["Ping", f"{ping} ms"]]
    table = tabulate(data, headers=["Measurement", "Value"], tablefmt="pretty")
    return table

print(test_speed())
