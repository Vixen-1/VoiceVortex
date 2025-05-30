/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_BUYER_DATA_ID: string;
    readonly VITE_SUPPLIER_DATA_ID: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  