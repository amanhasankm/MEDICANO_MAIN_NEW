import streamlit as st
import requests

class Pharmacies:
    def __init__(self):
        self.geocoding_url = "https://nominatim.openstreetmap.org/search"
        self.reverse_geocode_url = "https://nominatim.openstreetmap.org/reverse"

    def get_coordinates(self, place_name):
        params = {
            'q': place_name,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }
        headers = {
            'User-Agent': 'PharmacyFinderApp/1.0'
        }

        try:
            response = requests.get(self.geocoding_url, params=params, headers=headers)
            response.raise_for_status()
            results = response.json()

            if results:
                location = results[0]
                return location['lat'], location['lon']
            else:
                st.error("Place not found. Please try another place.")
                return None, None
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            return None, None

    def reverse_geocode(self, lat, lon):
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        headers = {
            'User-Agent': 'PharmacyFinderApp/1.0'
        }
        try:
            response = requests.get(self.reverse_geocode_url, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get('display_name', 'No address available')
        except requests.RequestException:
            return 'Address lookup failed'

    def find_nearby_pharmacies(self, location, radius, include_clinics_and_hospitals):
        lat, lon = location
        overpass_url = "http://overpass-api.de/api/interpreter"

        if include_clinics_and_hospitals:
            query = f"""
            [out:json];
            (
              node["amenity"="pharmacy"](around:{radius},{lat},{lon});
              node["amenity"="hospital"](around:{radius},{lat},{lon});
              node["amenity"="clinic"](around:{radius},{lat},{lon});
            );
            out body;
            """
        else:
            query = f"""
            [out:json];
            (
              node["amenity"="pharmacy"](around:{radius},{lat},{lon});
            );
            out body;
            """

        try:
            response = requests.post(overpass_url, data=query)
            response.raise_for_status()
            return response.json().get("elements", [])
        except requests.RequestException as e:
            st.error(f"Overpass API request failed: {e}")
            return []

    def app(self):
        st.title("🧴 Nearby Pharmacy Finder")

        place_name = st.text_input("Enter a place name (e.g., Mangalore, India):", "Mangalore, India")
        radius = st.slider("Select radius (meters):", 100, 5000, 1000)
        include_hospitals = st.checkbox("Include nearby hospitals and clinics", value=True)

        if st.button("Find Pharmacies"):
            if place_name:
                with st.spinner("Finding location..."):
                    lat, lon = self.get_coordinates(place_name)

                    if lat and lon:
                        with st.spinner("Searching for pharmacies..."):
                            pharmacies = self.find_nearby_pharmacies((lat, lon), radius, include_hospitals)

                            if pharmacies:
                                st.header(f"Found {len(pharmacies)} services nearby:")
                                for place in pharmacies:
                                    tags = place.get('tags', {})
                                    name = tags.get('name', 'Unnamed')
                                    amenity = tags.get('amenity', 'Service')
                                    lat = place.get('lat')
                                    lon = place.get('lon')
                                    address = self.reverse_geocode(lat, lon)

                                    st.write(f"**🏥 {amenity.title()} Name:** {name}")
                                    st.write(f"📍 **Address:** {address}")
                                    st.write(f"🌍 [View on Map](https://www.google.com/maps?q={lat},{lon})")
                                    st.write("---")
                            else:
                                st.warning("No nearby pharmacies found.")
            else:
                st.warning("Please enter a valid place name.")
