import {getStationsMetadata} from "../backendServices/stations";
import absoluteUrl from 'next-absolute-url'

function generateSiteMap(urls: string[]) {
  return `<?xml version="1.0" encoding="UTF-8"?>
     <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     ${urls
    .map((url) => {
      return `
       <url>
           <loc>${url}</loc>
       </url>
     `;
    })
    .join('')}
   </urlset>
 `;
}

function SiteMap() {
  // getServerSideProps will do the heavy lifting
}

// @ts-ignore
export async function getServerSideProps({ req, res }) {
  const { origin } = absoluteUrl(req)
  const stations_metadata = await getStationsMetadata();
  const urls: string[] = [];
  urls.push(`${origin}/`);
  for (const station_group of stations_metadata.station_groups) {
    for (const station_relationship of station_group.station_to_station_groups) {
      const station = stations_metadata.stations.find(s => s.id === station_relationship.station_id);
      if(station) {
        urls.push(`${origin?.replace("http", "https")}/${station_group.slug}/${station.slug}`);
      }
    }
  }

  // We generate the XML sitemap with the posts data
  const sitemap = generateSiteMap(urls);

  res.setHeader('Content-Type', 'text/xml');
  // we send the XML to the browser
  res.write(sitemap);
  res.end();

  return {
    props: {},
  };
}

export default SiteMap;