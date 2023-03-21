package no.fintlabs;

import no.fintlabs.core.consumer.shared.ConsumerProps;
import no.vigoiks.resourceserver.security.FintJwtCoreConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

@EnableWebFluxSecurity()
public class SecurityConfiguration {

    @Value("${fint.integration.service.authorized-scope:vigo.no}")
    private String authorizedScope;

    private ConsumerProps consumerProps;

    public SecurityConfiguration(ConsumerProps consumerProps) {
        this.consumerProps = consumerProps;
    }

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        http
                .authorizeExchange((authorize) -> authorize
                        .pathMatchers("/**")
                        .hasAuthority("ORGID_" + consumerProps.getOrgId())
                        .anyExchange()
                        .authenticated()
                )
                .oauth2ResourceServer((resourceServer) -> resourceServer
                        .jwt()
                        .jwtAuthenticationConverter(new FintJwtCoreConverter())
                );
        return http.build();
    }
}