import streamlit as st
import requests

class AmbulanceFinder:
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
            'User-Agent': 'AmbulanceFinderApp/1.0'
        }
        try:
            response = requests.get(self.geocoding_url, params=params, headers=headers)
            response.raise_for_status()
            results = response.json()

            if results:
                location = results[0]
                return location['lat'], location['lon']
            else:
                st.error("Location not found.")
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
            'User-Agent': 'AmbulanceFinderApp/1.0'
        }
        try:
            response = requests.get(self.reverse_geocode_url, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get('display_name', 'No address available')
        except requests.RequestException:
            return 'Address lookup failed'

    def find_nearby_services(self, location, radius, include_hospitals):
        lat, lon = location
        overpass_url = "http://overpass-api.de/api/interpreter"

        if include_hospitals:
            query = f"""
            [out:json];
            (
              node["amenity"="ambulance_station"](around:{radius},{lat},{lon});
              node["emergency"="ambulance"](around:{radius},{lat},{lon});
              node["amenity"="hospital"](around:{radius},{lat},{lon});
              node["amenity"="clinic"](around:{radius},{lat},{lon});
            );
            out body;
            """
        else:
            query = f"""
            [out:json];
            (
              node["amenity"="ambulance_station"](around:{radius},{lat},{lon});
              node["emergency"="ambulance"](around:{radius},{lat},{lon});
            );
            out body;
            """

        try:
            response = requests.post(overpass_url, data=query)
            response.raise_for_status()
            results = response.json()
            return results.get("elements", [])
        except requests.RequestException as e:
            st.error(f"Overpass API request failed: {e}")
            return []

    def app(self):
        st.title("🚑 Emergency Ambulance Locator")

        place_name = st.text_input("Enter your location (city or address):", "Mangalore, India")
        radius = st.slider("Search radius (meters):", 1000, 20000, 10000)
        include_hospitals = st.checkbox("Include hospitals and clinics", value=True)

        if st.button("Find Ambulances"):
            with st.spinner("🔍 Locating nearby emergency services..."):
                lat, lon = self.get_coordinates(place_name)
                if lat and lon:
                    services = self.find_nearby_services((lat, lon), radius, include_hospitals)

                    if services:
                        st.success(f"Found {len(services)} service(s) near {place_name}")
                        st.header("Nearby Emergency Services:")
                        for s in services:
                            lat = s.get('lat')
                            lon = s.get('lon')
                            name = s.get('tags', {}).get('name', 'Unnamed Service')
                            amenity = s.get('tags', {}).get('amenity', 'Unknown')
                            address = self.reverse_geocode(lat, lon)

                            st.write(f"**🚑 Name:** {name} ({amenity})")
                            st.write(f"📍 **Address:** {address}")
                            st.write(f"🌍 [View on Map](https://www.google.com/maps?q={lat},{lon})")
                            st.write(f"📞 **Contact:** +91-9876543210")
                            st.write("---")
                    else:
                        st.warning("No ambulance or medical services found. Try increasing the radius or enabling hospital search.")
                else:
                    st.error("Could not retrieve coordinates for the location.")
