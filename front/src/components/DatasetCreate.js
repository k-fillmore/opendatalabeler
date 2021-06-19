import { React, useState } from "react";
import {
  InputGroup,
  ButtonGroup,
  FormControl,
  ToggleButton,
  Button,
} from "react-bootstrap";
import Dropzone from "./Dropzone";
import { v4 as uuid } from "uuid";

function DatasetCreate() {
  const [datasetId, setDatasetId] = useState(uuid());
  const [datasetName, setDatasetName] = useState("");
  const [datasetType, setDatasetType] = useState("Image");
  const [datasetSubtype, setDatasetSubtype] = useState("Classification");
  const [datasetItems, setDatasetItems] = useState([
    { path: "test123.img", label: "Yes" },
  ]);

  const datasetTypes = [
    { name: "Image", value: "Image" },
    { name: "Text", value: "Text" },
    { name: "Audio", value: "Audio" },
    { name: "Video", value: "Video" },
  ];

  function displayDatasetTypes() {
    if ((datasetType === "Image") | (datasetType === "Video")) {
      const subtypes = [
        { name: "Classification", value: "Classification" },
        { name: "2D Bounding Box", value: "2D Bounding Box" },
        { name: "3D Bounding Box", value: "3D Bounding Box" },
        { name: "Semantic Segmentation", value: "Semantic Segmentation" },
        { name: "Instance Segmentation", value: "Instance Segmentation" },
        { name: "Lines and Splines", value: "Lines and Splines" },
        { name: "Polygons", value: "Polygons" },
      ];
      return <>{generateSubtypeButtons(subtypes)}</>;
    } else if (datasetType === "Text") {
      const subtypes = [
        { name: "Name Entity Recognition ", value: "Name Entity Recognition " },
        { name: "Sentiment analysis", value: "Sentiment analysis" },
        { name: "Text Summarization", value: "Text Summarization" },
        { name: "Aspect mining", value: "Aspect mining" },
        { name: "Topic modeling", value: "Topic modeling" },
        { name: "Machine Translation", value: "Machine Translation" },
      ];
      return <>{generateSubtypeButtons(subtypes)}</>;
    } else if (datasetType === "Audio") {
      const subtypes = [];
      return <>{generateSubtypeButtons(subtypes)}</>;
    }
  }
  // function to generate group of radio buttons
  function generateDatasetButtons(buttonArray) {
    return (
      <>
        <InputGroup className="mb-3">
          <ButtonGroup toggle>
            Dataset Type:
            {buttonArray.map((type, idx) => (
              <ToggleButton
                variant="dark"
                key={idx}
                type="radio"
                variant="secondary"
                name="radio"
                value={type.name}
                checked={datasetType === type.value}
                onChange={(e) => setDatasetType(type.value)}
              >
                {type.name}
              </ToggleButton>
            ))}
          </ButtonGroup>
        </InputGroup>
      </>
    );
  }
  function generateSubtypeButtons(buttonArray) {
    return (
      <>
        <InputGroup className="mb-3">
          <ButtonGroup toggle>
            Problem Type:
            {buttonArray.map((type, idx) => (
              <ToggleButton
                key={idx}
                type="radio"
                variant="secondary"
                name="radio"
                value={type.value}
                checked={datasetSubtype === type.value}
                onChange={(e) => setDatasetSubtype(type.value)}
              >
                {type.name}
              </ToggleButton>
            ))}
          </ButtonGroup>
        </InputGroup>
      </>
    );
  }

  return (
    <div>
      <div>Dataset ID: {datasetId}</div>
      <InputGroup className="mb-3">
        <InputGroup.Prepend>
          <InputGroup.Text id="basic-addon1" value={datasetName}>
            Name
          </InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl
          placeholder="Name"
          aria-label="Name"
          aria-describedby="basic-addon1"
          value={datasetName}
          onChange={(e) => setDatasetName(e.target.value)}
        />
      </InputGroup>
      <div>{generateDatasetButtons(datasetTypes)}</div>
      <div>{displayDatasetTypes()}</div>
      <div><Dropzone></Dropzone></div>
      <div>
        <Button variant="dark">Create</Button>
      </div>
    </div>
  );
}

export default DatasetCreate;