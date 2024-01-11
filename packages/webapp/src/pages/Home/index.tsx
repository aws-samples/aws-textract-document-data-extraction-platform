/*! Copyright [Amazon.com](http://amazon.com/), Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0 */
import {
  Container,
  ContentLayout,
  Header,
  SpaceBetween,
  // Spinner,
} from "@cloudscape-design/components";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
// import { useSayHello } from "myapi-typescript-react-query-hooks";

/**
 * Component to render the home "/" route.
 */
const Home: React.FC = () => {
  const navigate = useNavigate();
  useEffect(() => navigate("/apiExplorer"), []);
  // const sayHello = useSayHello({ name: "World" });

  return (
    <ContentLayout header={<Header>Home</Header>}>
      <SpaceBetween size="l">
        <Container>
          Hello World!
          {/* {sayHello.isLoading ? <Spinner /> : <>{sayHello.data?.message}</>} */}
        </Container>
      </SpaceBetween>
    </ContentLayout>
  );
};

export default Home;

