import {
  DefaultApi,
  Configuration,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import useSigV4Client from "@aws-northstar/ui/components/CognitoAuth/hooks/useSigv4Client";
import { useContext, useMemo } from "react";
import { RuntimeConfigContext } from "../components/RuntimeContext";

export const useDefaultApiClient = () => {
  const client = useSigV4Client();
  const runtimeContext = useContext(RuntimeConfigContext);

  return useMemo(() => {
    return runtimeContext?.apiUrl
      ? new DefaultApi(
          new Configuration({
            basePath: runtimeContext.apiUrl,
            fetchApi: client,
          }),
        )
      : undefined;
  }, [client, runtimeContext?.apiUrl]);
};
