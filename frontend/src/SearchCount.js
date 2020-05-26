import React from "react";
import "./SearchCount.css";

function SearchCount(props) {
    function getChildren() {
        let elements = [];

        if (props.resultIndex > 0) {
            elements.push(
                <button key="prevButton" onClick={props.showPrevious}>
                    Previous
                </button>
            );
        }
        console.log(props);

        elements.push(
            <span key="text">
                Showing result {props.resultIndex} out of {props.results.count}{" "}
                for "{props.terms}"
            </span>
        );

        if (props.resultIndex < props.results.count - 1) {
            elements.push(
                <button key="nextButton" onClick={props.showNext}>
                    Next
                </button>
            );
        }

        return elements;
    }

    if (!props.results) {
        return (
            <div className="SearchCount">
                Enter search terms and press &lt;Enter&gt; to see results
            </div>
        );
    }

    if (!props.results.count) {
        return (
            <div className="SearchCount">
                No results found for "{props.terms}"
            </div>
        );
    }

    return <div className="SearchCount">{getChildren()}</div>;
}

export default SearchCount;
