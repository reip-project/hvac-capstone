import reip
import reip.blocks as B
from sensor import SHTC3

if __name__ == "__main__":
    # Pipeline definition
    with reip.Graph() as graph:
        # Capture data in an independent process
        # using Task context to prevent data loss
        with reip.Task("Sensor"):
            sensor = SHTC3(name="SHTC3", max_rate=1)

        B.output.Csv("data/test.csv", name="Writer", headers=["temp", "hum"], max_rows=100)(sensor)

    # Run the pipeline
    graph.run()
