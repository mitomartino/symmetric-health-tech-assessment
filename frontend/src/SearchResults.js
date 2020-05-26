import React from "react";
import { useEffect, useState } from "react";
import "./SearchResults.css";

function SearchResults(props) {
    const [header, setHeader] = useState([]);

    function renderHeader() {
        let entry = {
            lineNum: 0,
            values: header.map(() => ""),
        };

        return renderResult(entry);
    }

    function renderResult(result) {
        return result.values.map(renderAttr);
    }

    function renderAttr(attr, index) {
        return [
            <div key="header-{index}" className="SearchResults-header-cell">
                {header[index]}
            </div>,
            <div key="value-{index}" className="SearchResults-body-attr">
                {attr}
            </div>,
        ];
    }

    // fetch header data only on first render
    useEffect(() => {
        (async () => {
            const rawData = await fetch("/header", {
                headers: { Accept: "application/json" },
            });

            var data = JSON.parse(await rawData.text());
            setHeader(data.header);
        })();
    }, []);

    if (!header) {
        return <div className="SearchResults"></div>;
    }

    if (!props.results || !props.results.entries.length) {
        return <div className="SearchResults">{renderHeader()}</div>;
    }

    return (
        <div className="SearchResults">
            {renderResult(props.results.entries[props.resultIndex])}
        </div>
    );
}

export default SearchResults;
