import React, { useState, useEffect } from 'react';
import PlacesAutocomplete from 'react-places-autocomplete';
import './AutocompleteAddressInput.css';

const AutocompleteAddressInput = ({ onSelect , onChange}) => {
  const [address, setAddress] = useState('');
  const [coordinates, setCoordinates] = useState({ latitude: null, longitude: null });

  const handleChange = (newAddress) => {
    setAddress(newAddress);
    onChange(newAddress);
  };

  const handleSelect = (location) => {
    setCoordinates(location);
    onSelect(location);
  };

  useEffect(() => {
    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results.length > 0) {
        const { lat, lng } = results[0].geometry.location;
        handleSelect({ latitude: lat(), longitude: lng() });
      } else {
        handleSelect({ latitude: null, longitude: null });
      }
    });
  }, [address]);

  return (
    <div className="AutocompleteAddressInput">
      <PlacesAutocomplete value={address} onChange={handleChange} onSelect={setAddress}>
        {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
          <div>
            <input
              {...getInputProps({
                placeholder: 'Enter your address',
                className: 'address-input',
              })}
            />
            <div className="autocomplete-dropdown-container">
              {loading && <div>Loading...</div>}
              {suggestions.map((suggestion) => {
                const className = suggestion.active ? 'suggestion-item--active' : 'suggestion-item';
                return (
                  <div
                    {...getSuggestionItemProps(suggestion, {
                      className,
                    })}
                  >
                    <span>{suggestion.description}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </PlacesAutocomplete>
    </div>
  );
};

export default AutocompleteAddressInput;
