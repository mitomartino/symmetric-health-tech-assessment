import React from "react";
import { useState } from "react";
import "./SearchBox.css";

function SearchBox(props) {
    const [terms, setTerms] = useState(null);

    function handleTextChange(evt) {
        setTerms(evt.target.value);
    }

    function keyPressed(evt) {
        if (terms && evt.key === "Enter") {
            props.onSearch(terms);
        }
    }

    function search() {
        if (terms) {
            props.onSearch(terms);
        }
    }

    return (
        <div className="SearchBox">
            <input
                className="SearchBox-input"
                type="text"
                name="terms"
                placeholder="Please enter some search terms"
                onChange={handleTextChange}
                onKeyPress={keyPressed}
            />
            <button
                className="SearchBox-button"
                type="button"
                name="searchButton"
                disabled={!terms}
                onClick={search}
            >
                Search
            </button>
        </div>
    );
}

export default SearchBox;
