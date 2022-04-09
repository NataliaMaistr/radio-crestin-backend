import {config} from "dotenv";

config();

export const PROJECT_ENV: {
    APP_SERVER_PORT: number
    APP_GRAPHQL_ENDPOINT_URI: string
    APP_GRAPHQL_ADMIN_SECRET: string
    APP_REFRESH_STATIONS_METADATA_CRON: string
} = {
    APP_SERVER_PORT: parseInt(process.env.APP_SERVER_PORT || "8080"),
    APP_GRAPHQL_ENDPOINT_URI: process.env.APP_GRAPHQL_ENDPOINT_URI || "",
    APP_GRAPHQL_ADMIN_SECRET: process.env.APP_GRAPHQL_ADMIN_SECRET || "",
    APP_REFRESH_STATIONS_METADATA_CRON: process.env.APP_REFRESH_STATIONS_METADATA_CRON || "*/10 * * * * *",
}