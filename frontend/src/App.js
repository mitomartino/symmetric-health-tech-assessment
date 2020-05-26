import React from "react";
import { useState } from "react";
import "./App.css";
import SearchBox from "./SearchBox";
import SearchResults from "./SearchResults";
import SearchCount from "./SearchCount";

function App() {
    const [data, setData] = useState(null);
    const [terms, setTerms] = useState("");
    const [resultIndex, setResultIndex] = useState(0);

    const doSearch = (terms) => {
        (async () => {
            const urlTerms = encodeURIComponent(terms);

            const rawData = await fetch(`/data?terms=${urlTerms}`, {
                headers: { Accept: "application/json" },
            });

            const jsonData = await rawData.text();
            setTerms(terms);
            setData(JSON.parse(jsonData));
            setResultIndex(0);
        })();
    };

    const nextResult = () => {
        if (data && resultIndex < data.count - 1) {
            console.log("setResultIndex");
            setResultIndex(resultIndex + 1);
        }
    };

    const prevResult = () => {
        if (data && resultIndex > 0) {
            setResultIndex(resultIndex - 1);
        }
    };

    return (
        <div className="App">
            <div className="App-header">
                <img
                    className="App-logo"
                    alt="Symmetric Healthcare"
                    src="logo192.png"
                ></img>
                <div className="App-titlebar full-flex">
                    Symmetric Healthcare Technical Assessment
                </div>
            </div>

            <div className="App-body">
                <SearchBox onSearch={doSearch}></SearchBox>
                <SearchResults
                    results={data}
                    resultIndex={resultIndex}
                ></SearchResults>
                <SearchCount
                    results={data}
                    terms={terms}
                    resultIndex={resultIndex}
                    showNext={nextResult}
                    showPrevious={prevResult}
                ></SearchCount>
            </div>
        </div>
    );
}

export default App;
